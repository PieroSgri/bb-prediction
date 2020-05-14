import csv
import os

import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image

FRAME_DATA_PATH = "tmp/frame_data.txt"
RESULTS_PATH = "results/"

image_height = 0   # Initialized for later use
image_width = 0    # Initialized for later use
frame_list = []    # Initialized for later use


class Frame:
    def __init__(self, image_data, height, width):
        self.image_data = image_data
        self.height = height
        self.width = width
        # Black Magic!
        composite_list = [image_data[x:x + image_width] for x in range(0, len(image_data), image_width)]
        self.image_matrix = np.array(composite_list)  # Create numpy array froma list of list
        assert(self.image_matrix.shape == (height, width))
        print("Built numpy array of shape", self.image_matrix.shape)
        frame_list.append(self)


def listener():

    if os.path.exists(FRAME_DATA_PATH):
        os.remove(FRAME_DATA_PATH)

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/dvs/image_raw', Image, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


def callback(image_msg):
    # rospy.loginfo(rospy.get_caller_id() + 'I heard %s', image_msg)
    global image_height  # To modify variables in outer scope
    global image_width   # To modify variables in outer scope
    image_height = image_msg.height
    image_width = image_msg.width
    write_data(image_msg.data)


def write_data(data):
    ASCII_values = []
    for character in data:
        ASCII_values.append(ord(character))  # convert into ASCII value

    # print(ASCII_values)

    with open(FRAME_DATA_PATH, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(ASCII_values)


def build_frames():
    with open(FRAME_DATA_PATH, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            Frame(row, image_height, image_width)

        count = 1
        for frame in frame_list:
            frame_name = (RESULTS_PATH + str(count) + ".jpg")
            img = frame.image_matrix.astype(np.uint8)
            cv2.imwrite(frame_name, img)
            print("Built", frame_name)
            count += 1


listener()

build_frames()

print ("Completed")
