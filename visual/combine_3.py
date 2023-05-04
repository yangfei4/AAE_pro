# combine 3 images vertically
# input: path
# 3 images are 1.png, 2.png and 3.png
# output: 123.png

import sys
import os
import cv2
import numpy as np

# get path from command line
path = sys.argv[1]

# read images
img1 = cv2.imread(os.path.join(path, '1.png'))
img2 = cv2.imread(os.path.join(path, '2.png'))
img3 = cv2.imread(os.path.join(path, '3.png'))

# combine images with 20 white pixel in between

img_combined = np.concatenate((img1, 255*np.ones((img1.shape[0], 20, 3), np.uint8), img2, 255*np.ones((img1.shape[0], 20, 3), np.uint8), img3), axis=1)
# img_combined = np.concatenate((img1, np.ones((0, img1.shape[1], 3), dtype=np.uint8)*255, img2, np.ones((0, img1.shape[1], 3), dtype=np.uint8)*255, img3), axis=0)

# write image
cv2.imwrite(os.path.join(path, '123.png'), img_combined)
cv2.imshow('image', img_combined)
cv2.waitKey(0)