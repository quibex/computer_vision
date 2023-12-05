import cv2
import numpy as np
import os
import time
#from comp_vision.yolo.bag2video import getVideoFromBag
#from bag2video import getVideoFromBag

def findObj(outputs, frame, confThreshold, nmsThreshold, classNames, non_access_arr):
    hT, wT, cT = frame.shape
    boxes = []
    classIds = []
    confidence_value = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(detection[2] * wT), int(detection[3] * hT)
                x, y = int((detection[0] * wT) - w / 2), int((detection[1] * hT) - h / 2)
                boxes.append([x, y, w, h])
                classIds.append(classId)
                confidence_value.append(float(confidence))

    # print(boxes)

    boxes_to_keep = cv2.dnn.NMSBoxes(boxes, confidence_value, confThreshold, nmsThreshold)
    boxes_to_keep = [x[0] for x in boxes_to_keep]
    #print(boxes_to_keep)


    necessary_boxes = []
    for i in boxes_to_keep:
        box = boxes[i]

        #print(box)
        x, y, w, h = box[0], box[1], box[2], box[3]
        #print()
        if classNames[classIds[i]].upper() in non_access_arr:  # Check for only food and person
            necessary_boxes.append([x, y, w, h, [i, classIds[i], confidence_value[i]]])
            #
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
            # cv2.putText(frame, f"{classNames[classIds[i]].upper()} {confidence_value[i] * 100:.2f}%",
            #             (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    boxes_into_out = []
    OnlyPerson = True
    ProductConf = 0
    HumanConf = 0
    for person in necessary_boxes:    # Square in square checking
        if person[4][1] != 0:
            continue
        boxes_into_out.append(person)
        for product in necessary_boxes:
            if product == person:
                continue
            if person[0] - product[0] <= 50 and person[1] - product[1] <= 50:        # [x, y]
                if person[0] + person[2] >= product[0] + product[2] - 50 and person[1] + person[3] >= product[1] + product[3] - 50:  # [x1, y1]
                    OnlyPerson = False
                    
                    boxes_into_out.append(product)
                    ProductConf += product[4][2]
                    HumanConf += person[4][2]
    if len(boxes_into_out) > 0 and not(OnlyPerson):
        
        x = min(boxes_into_out, key=lambda x: x[0])
        y = min(boxes_into_out, key=lambda x: x[1])
        w = max(boxes_into_out, key=lambda x: x[2])
        h = max(boxes_into_out, key=lambda x: x[3])
        typeOfProduct = [x for x in boxes_into_out if x[4][1] != 0][0][4][1]
    # y = max([x[1] for x in boxes_into_out])
    # w = max([x[2] for x in boxes_into_out])
    # h = max([x[3] for x in boxes_into_out])
        cv2.rectangle(frame, (x[0], y[1]), (x[0] + w[2], y[1] + h[3]), (0, 0, 255), 2)
        cv2.putText(frame, f"PERSON WITH {classNames[typeOfProduct].upper()} {ProductConf * HumanConf * 100:.2f}%",
                    (x[0] + 7, round(y[1] + h[3] / 2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    if len(boxes_into_out) > 0 and OnlyPerson:
        for person in boxes_into_out:
            x, y, w, h, settings = person
            _, classId, confValue = settings
            print(classId, confValue)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{classNames[classId].upper()} {confValue * 100:.2f}%",
                        (x + 7, round(y + h / 2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

def SaveVideoFile(input_file_name, user_id, pathToSave="files/mp4", filePATH="files/"):
    print("=====================")
    print(user_id)
    print("=====================")

    input_file_name = filePATH + str(input_file_name)


    if os.path.basename(rf'{input_file_name}').split(".")[1] == "bag":
        print(input_file_name)
        print(os.path.dirname(os.path.abspath(input_file_name)))
        os.system(f"python3 /workspace/comp_vision/yolo/bag2video.py {input_file_name} /workspace/files/bag_files")
        #getVideoFromBag(input_file_name)
        input_file_name = os.path.dirname(os.path.abspath(input_file_name)) + "/" + os.path.basename(rf'{input_file_name}').split(".")[0] + ".mp4"
    print("IM HERE!!!!!!!!!!!")
    # Yolo settings and files
    modelWeights = "comp_vision/yolo/yolov3.weights"
    modelCFG = "comp_vision/yolo/yolov3.cfg"
    classesFile = "comp_vision/yolo/coco.names"
    non_access_products = "comp_vision/yolo/search.names"
    
    #modelWeights = "yolov3.weights"
    #modelCFG = "yolov3.cfg"
    #classesFile = "coco.names"
    #non_access_products = "search.names"
    
    confThreshold = 0.5
    nmsThreshold = 0.3

    with open(classesFile) as f:
        classNames = f.read().split("\n")

    with open(non_access_products) as f:
        non_access_arr = [x.upper() for x in f.read().split()]

    # Name of video file
    output_file_name = os.path.basename(rf'{input_file_name}')
    output_file_name = pathToSave + "/" + output_file_name[:output_file_name.index('.')] + "_" + str(user_id) + ".mp4"
    
    #output_file_name = output_file_name[:output_file_name.index('.')] + "_" + str(user_id) + ".mp4"
    print(output_file_name, input_file_name)
    
    # Turn on yolo
    net = cv2.dnn.readNetFromDarknet(modelCFG, modelWeights)

    # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    # Opening input video-file
    cap = cv2.VideoCapture(input_file_name)
    whT = 608  # Downgrade resolution for yolo

    total_frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cur_frame = 0

    # Creating video object
    source_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Getting source width
    source_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Getting source height
    source_fps = int(cap.get(cv2.CAP_PROP_FPS))  # Getting source fps

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    ml_video = cv2.VideoWriter(output_file_name, fourcc, source_fps, (source_width, source_height))
    #print(total_frame_num)
    #time1 = time.time()
    while cur_frame < total_frame_num:
        success, frame = cap.read()
        blob = cv2.dnn.blobFromImage(frame, 1/255, (whT, whT), [0, 0, 0], 1, crop=False)
        net.setInput(blob)

        layerNames = net.getLayerNames()

        #outputNames = [layerNames[i] for i in (net.getUnconnectedOutLayers() - 1)]
        outputNames = net.getUnconnectedOutLayersNames()

        #print(outputNames)
        outputs = net.forward(outputNames)

        findObj(outputs, frame, confThreshold, nmsThreshold, classNames, non_access_arr)
        ml_video.write(frame)

        # cv2.imshow(input_file_name, frame)
        # cv2.waitKey(1)

        print(cur_frame, total_frame_num)
        #print(round((cur_frame / total_frame_num) * 100, 2),"%")
        cur_frame += 1

    ml_video.release()
    cap.release()
    cv2.destroyAllWindows()
    print("=============================")
    print(output_file_name)
    print("=============================")
    #transcoded_video = os.path.dirname(output_file_name) + "/" + os.path.basename(output_file_name).split(".")[0] + "_transcoded" + ".mp4"
    transcoded_video = pathToSave + "/" + os.path.basename(output_file_name).split(".")[0] + "_transcoded" + ".mp4"
    print(transcoded_video)
    # ffmpeg -hwaccel cuda -loglevel warning -y -i short.mp4 -vcodec libx264 short_264.mp4
    os.system(f"ffmpeg -y -nostdin -i {output_file_name} -vcodec libx264 {transcoded_video}")

    os.remove(output_file_name)
    return transcoded_video[6:]


def getBagVideo(pathToBag, user_id, mode, pathToSave="files/mp4"):
    input_file_name = "files/" + str(pathToBag)
    output_file_name = pathToSave + "/" + os.path.basename(input_file_name).split(".")[0] + "_" + str(user_id) + "_" + mode + ".mp4"
    
    os.system(f"python3 /workspace/comp_vision/yolo/bag2video.py {input_file_name} {output_file_name} {mode}")
    return output_file_name[6:]
    
#getDepthVideo("/workspace/small.bag", "6")

#print(SaveVideoFile("current.bag", 321, pathToSave="", filePATH=""))


