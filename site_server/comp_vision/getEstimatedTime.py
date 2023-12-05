import rosbag
import cv2
import os


def getEstimatedTime(path):
    if os.path.basename(path).split(".")[1] == "bag":
        bag = rosbag.Bag(path)
        total_frame_num = bag.get_message_count("/device_0/sensor_1/Color_0/image/data")
        return total_frame_num
    if os.path.basename(path).split(".")[1] != "bag":
        cap = cv2.VideoCapture(path)
        total_frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return total_frame_num





