import cv2
try:
    import tensorflow.compat.v1 as tf
    tf.disable_eager_execution()
except:
    import tensorflow as tf
import numpy as np
import glob
import os
import time
import argparse
import configparser
import json
import re

from auto_pose.ae import factory, utils

# def extract_number(file_name):
#     # match = re.search(r'(\d+)/2_roi/\d+\.png$', file_name)
#     match = re.search(r'(\d+)/2_roi/\d+\.png$', file_name)
#     return int(match.group(1)) if match else None

def extract_number(file_name):
    match = re.search(r'(\d+)\.png$', file_name)
    return int(match.group(1)) if match else None

parser = argparse.ArgumentParser()
parser.add_argument("experiment_name")
parser.add_argument("-f", "--file_str", required=True, help='folder or filename to image(s)')
# parser.add_argument("-gt_bb", action='store_true', default=False)
arguments = parser.parse_args()
full_name = arguments.experiment_name.split('/')
experiment_name = full_name.pop()
experiment_group = full_name.pop() if len(full_name) > 0 else ''

file_str = arguments.file_str
if os.path.isdir(file_str):
    files = sorted(glob.glob(os.path.join(str(file_str),'*.png'))+glob.glob(os.path.join(str(file_str),'*.jpg')))
else:
    files = [file_str]

workspace_path = os.environ.get('AE_WORKSPACE_PATH')
if workspace_path == None:
    print('Please define a workspace path:\n')
    print('export AE_WORKSPACE_PATH=/path/to/workspace\n')
    exit(-1)
log_dir = utils.get_log_dir(workspace_path,experiment_name,experiment_group)
ckpt_dir = utils.get_checkpoint_dir(log_dir)

codebook, dataset = factory.build_codebook_from_name(experiment_name, experiment_group, return_dataset=True)

gpu_options = tf.GPUOptions(allow_growth=True, per_process_gpu_memory_fraction = 0.9)
config = tf.ConfigProto(gpu_options=gpu_options)
config.gpu_options.allow_growth = True

data = {}
objID = int(re.search(r"(\d+)_roi", file_str).group(1))
dir_name = f"{objID}_pred"

scene_path = os.path.dirname(file_str)
pred_path = f"{scene_path}/{objID}_pred"

os.makedirs(pred_path, exist_ok=True)

with tf.Session(config=config) as sess:

    factory.restore_checkpoint(sess, tf.train.Saver(), ckpt_dir)

    for file in files:
        im = cv2.imread(file)
        im = cv2.resize(im,(128,128))

        R = codebook.nearest_rotation(sess, im)
        print(R)
        
        number = extract_number(file)

        pred_view = dataset.render_rot( R,downSample = 1)
        cv2.imwrite(f"{pred_path}/{str(number)}.png", pred_view)

        # cv2.imshow('resized img', cv2.resize(im/255.,(256,256)))
        # cv2.imshow('pred_view', cv2.resize(pred_view,(256,256)))
        # cv2.waitKey(0)
        # print(file[-7:])
        # print(number)
        if number is not None:
            # Save the rotation matrix in the dictionary with the number as the key
            data[str(number)] = R.reshape(-1).tolist()

with open(f"{scene_path}/{dir_name}.json", 'w') as json_file:
    json.dump(data, json_file)

# import cv2
# try:
#     import tensorflow.compat.v1 as tf
#     tf.disable_eager_execution()
# except:
#     import tensorflow as tf
# import numpy as np
# import glob
# import os
# import time
# import argparse
# import configparser

# from auto_pose.ae import factory, utils



# parser = argparse.ArgumentParser()
# parser.add_argument("experiment_name")
# parser.add_argument("-f", "--file_str", required=True, help='folder or filename to image(s)')
# # parser.add_argument("-gt_bb", action='store_true', default=False)
# arguments = parser.parse_args()
# full_name = arguments.experiment_name.split('/')
# experiment_name = full_name.pop()
# experiment_group = full_name.pop() if len(full_name) > 0 else ''

# file_str = arguments.file_str
# if os.path.isdir(file_str):
#     files = sorted(glob.glob(os.path.join(str(file_str),'*.png'))+glob.glob(os.path.join(str(file_str),'*.jpg')))
# else:
#     files = [file_str]

# workspace_path = os.environ.get('AE_WORKSPACE_PATH')
# if workspace_path == None:
#     print('Please define a workspace path:\n')
#     print('export AE_WORKSPACE_PATH=/path/to/workspace\n')
#     exit(-1)
# log_dir = utils.get_log_dir(workspace_path,experiment_name,experiment_group)
# ckpt_dir = utils.get_checkpoint_dir(log_dir)

# codebook, dataset = factory.build_codebook_from_name(experiment_name, experiment_group, return_dataset=True)

# gpu_options = tf.GPUOptions(allow_growth=True, per_process_gpu_memory_fraction = 0.9)
# config = tf.ConfigProto(gpu_options=gpu_options)
# config.gpu_options.allow_growth = True

# with tf.Session(config=config) as sess:

#     factory.restore_checkpoint(sess, tf.train.Saver(), ckpt_dir)

#     for file in files:
#         im = cv2.imread(file)
#         im = cv2.resize(im,(128,128))

#         R = codebook.nearest_rotation(sess, im)
#         print(R)

#         pred_view = dataset.render_rot( R,downSample = 1)
    
#         cv2.imshow('resized img', cv2.resize(im/255.,(256,256)))
#         cv2.imshow('pred_view', cv2.resize(pred_view,(256,256)))
#         cv2.waitKey(0)


