# combine 2 images
# input path/filename
# 2 images are filename_in.png and filename_out.png 
# output $file_name_combined.png

import sys
import os
import cv2
import numpy as np

# get filename from command line
file_name = sys.argv[1]
file_name_in = file_name + '_in.png'
file_name_out = file_name + '_out.png'
file_name_combined = file_name + '_combined.png'

# read images
img_in = cv2.imread(file_name_in)
img_out = cv2.imread(file_name_out)

# combine images with no white pixel in between
img_combined = np.concatenate((img_in, img_out), axis=1)


# write image
cv2.imwrite(file_name_combined, img_combined)
cv2.imshow('image', img_combined)
# cv2.waitKey(0)
