# combine 3 images vertically
# input: path
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


img_combined = np.concatenate((img1, 255*np.ones((img1.shape[0], 0, 3), np.uint8), img2, 255*np.ones((img1.shape[0], 0, 3), np.uint8), img3), axis=1)

# write image
cv2.imwrite(os.path.join(path, '123.png'), img_combined)
cv2.imshow('image', img_combined)
cv2.waitKey(0)