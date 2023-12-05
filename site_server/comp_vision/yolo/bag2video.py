import pyrealsense2 as rs
import rosbag
import time
import subprocess as sp
import os
import sys

DataTopic = "/device_0/sensor_1/Color_0/image/data"


def WriteFrame(msg, topic, t, pixel_encoding, t_first, t_file, t_video, frame_list, output_filename, fps=30,CONVERTER="ffmpeg", ):
    if len(msg.data) == 0:
        return
    if topic not in t_first:
        t_first[topic] = t
        t_video[topic] = 0
        t_file[topic] = 0

    t_file[topic] = (t - t_first[topic]).to_sec()
    # print("HERE")
    while t_video[topic] < t_file[topic]:
        if topic not in frame_list:

            size = str(msg.width) + "x" + str(msg.height)
            cmd = [CONVERTER, '-v', '1', '-stats', '-r', str(fps), '-f', 'rawvideo', '-s', size,
                   '-pix_fmt', pixel_encoding, '-i', '-', '-an', output_filename]
            frame_list[topic] = sp.Popen(cmd, stdin=sp.PIPE)

        frame_list[topic].stdin.write(msg.data)
        t_video[topic] += 1 / fps


def FltImgMsg(topic, datatype, md5sum, msg_def, header):
    if datatype == "sensor_msgs/Image":
        if DataTopic == topic:
            return True
    return False


def getVideoFromBag(FileFrom, FileTo="/workspace/files/bag_files", user_id="", mode="rgb"):
    time1 = time.time()

    print(FileFrom)
    # filename = "../current.bag"
    if mode == "depth":
        global DataTopic
        DataTopic = "/device_0/sensor_0/Depth_0/image/data"

    # Create a config object
    pipeline = rs.pipeline()
    config = rs.config()
    rs.config.enable_device_from_file(config, FileFrom)
    profile = pipeline.start(config)

    # Settings
    fps = int([x for x in str(profile.get_stream(rs.stream.color)).split() if "fps" in x][0][:-3])

    output_filename = os.path.basename(rf'{FileFrom}')
    #output_filename = os.path.dirname(os.path.abspath(FileFrom)) + "/" + output_filename[:output_filename.index('.')] + str(user_id) + ".mp4"
    output_filename = "." + "/" + output_filename[:output_filename.index('.')] + str(user_id) + ".mp4"
    t_first = {}
    t_file = {}
    t_video = {}
    frame_list = {}

    bag = rosbag.Bag(FileFrom)

    for topic, msg, t in bag.read_messages(connection_filter=FltImgMsg):
        try:
            pixel_encoding = None
            #print(msg.encoding)
            if msg.encoding.find("bgr8") != -1:
                pixel_encoding = "bgr8"
            elif msg.encoding.find("rgb8") != -1:
                pixel_encoding = "rgb24"
            elif msg.encoding.find("mono16") != -1:
                pixel_encoding = "gray16le"

            if pixel_encoding:
                WriteFrame(msg, topic, t, pixel_encoding, t_first, t_file, t_video, frame_list, output_filename, fps)

        except Exception as E:
            print(E)
            
    print("Video extracted")
    print(os.path.abspath(output_filename))
    os.system(f"mv {os.path.abspath(output_filename)} {FileTo}")
    print(time.time() - time1)
    return output_filename
print(sys.argv)
if len(sys.argv) == 4:
    getVideoFromBag(sys.argv[1], sys.argv[2], mode=sys.argv[3])
elif len(sys.argv) == 5:
    getVideoFromBag(sys.argv[1],  sys.argv[2], mode=(sys.argv[3]).lower(), user_id=sys.argv[4])
else:
    getVideoFromBag(sys.argv[1],  sys.argv[2])














