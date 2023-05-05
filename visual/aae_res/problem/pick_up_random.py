import os
import random
import sys
import cv2
import numpy as np

def pick_random_images(folder_path, num_picks=2):
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    # selected_images = random.sample(image_files, num_picks)

    return image_files

def main():
    nums = {'1','2','5','12','14','15','16','18','27','29'}

    for num in nums:
        folder_path_1 = f"./{num}_roi"
        folder_path_2 = f"./{num}_gt"
        folder_path_3 = f"./{num}_pred"
        folder_path_4 = f"./{num}_combined"

        selected_images = pick_random_images(folder_path_1)

        for image_name in selected_images:
            img1 = cv2.imread(os.path.join(folder_path_1, image_name))
            # reshape img1 to 128x128
            img1 = cv2.resize(img1, (128, 128))
            img2 = cv2.imread(os.path.join(folder_path_2, image_name))
            img3 = cv2.imread(os.path.join(folder_path_3, image_name))
            print(image_name)
            img_combined = np.concatenate((img1, 255*np.ones((img1.shape[0], 0, 3), np.uint8), img2, 255*np.ones((img1.shape[0], 0, 3), np.uint8), img3), axis=1)
            # make dir of folder_path_4 if not exist
            if not os.path.exists(folder_path_4):
                os.makedirs(folder_path_4)
            # write image
            cv2.imwrite(os.path.join(folder_path_4, image_name), img_combined)
            # cv2.imshow('image', img_combined)
            # cv2.waitKey(0)

if __name__ == '__main__':
    main()
