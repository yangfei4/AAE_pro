# rendomly choose 9 .jpg images and resize them to 500x375 from a folder and combine them into 3x3 grid
# input: path
# output: the combined image saved as 9.png

import sys
import os
import cv2
import numpy as np
import random

# get path from command line
path = sys.argv[1]

# read images
img_list = []
for file in os.listdir(path):
    if file.endswith('.jpg'):
        img_list.append(file)
img_list = random.sample(img_list, 9)
img1 = cv2.imread(os.path.join(path, img_list[0]))
img2 = cv2.imread(os.path.join(path, img_list[1]))
img3 = cv2.imread(os.path.join(path, img_list[2]))
img4 = cv2.imread(os.path.join(path, img_list[3]))
img5 = cv2.imread(os.path.join(path, img_list[4]))
img6 = cv2.imread(os.path.join(path, img_list[5]))
img7 = cv2.imread(os.path.join(path, img_list[6]))
img8 = cv2.imread(os.path.join(path, img_list[7]))
img9 = cv2.imread(os.path.join(path, img_list[8]))

# combine images with 10 white pixel in between

# resize images to 500x375
img1 = cv2.resize(img1, (500, 375))
img2 = cv2.resize(img2, (500, 375))
img3 = cv2.resize(img3, (500, 375))
img4 = cv2.resize(img4, (500, 375))
img5 = cv2.resize(img5, (500, 375))
img6 = cv2.resize(img6, (500, 375))
img7 = cv2.resize(img7, (500, 375))
img8 = cv2.resize(img8, (500, 375))
img9 = cv2.resize(img9, (500, 375))



img_combined = np.concatenate((img1, 255*np.ones((img1.shape[0], 10, 3), np.uint8), img2, 255*np.ones((img1.shape[0], 10, 3), np.uint8), img3), axis=1)
img_combined = np.concatenate((img_combined, 255*np.ones((10, img1.shape[1]*3+20*2, 3), np.uint8)), axis=0)
img_combined = np.concatenate((img_combined, img4, 255*np.ones((img1.shape[0], 10, 3), np.uint8), img5, 255*np.ones((img1.shape[0], 10, 3), np.uint8), img6), axis=1)
img_combined = np.concatenate((img_combined, 255*np.ones((10, img1.shape[1]*3+20*2, 3), np.uint8)), axis=0)
img_combined = np.concatenate((img_combined, img7, 255*np.ones((img1.shape[0], 10, 3), np.uint8), img8, 255*np.ones((img1.shape[0], 10, 3), np.uint8), img9), axis=1)

# write image
cv2.imwrite("~/9.png", img_combined)
cv2.imshow('image', img_combined)
cv2.waitKey(0)