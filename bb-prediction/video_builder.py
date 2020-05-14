import cv2
import os

RESULTS_PATH = "results/"
VIDEO_NAME = RESULTS_PATH + "gen_video.mp4"

list_of_files = os.listdir(RESULTS_PATH)
list_of_files = sorted(list_of_files, key=lambda f: int(filter(str.isdigit, f)))  # Black Magic!

# Read first image of list to get image shape
sample = cv2.imread(RESULTS_PATH + list_of_files[0])
height, width, layers = sample.shape

# Codec and settings
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(VIDEO_NAME, fourcc, 30, (width, height))

for image in list_of_files:
    frame = cv2.imread(RESULTS_PATH + image)
    video.write(frame)

cv2.destroyAllWindows()
video.release()

print("Built video at:", VIDEO_NAME)
