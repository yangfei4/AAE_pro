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

from auto_pose.ae import factory, utils



parser = argparse.ArgumentParser()
parser.add_argument("experiment_name")
# parser.add_argument("-gt_bb", action='store_true', default=False)
arguments = parser.parse_args()
full_name = arguments.experiment_name.split('/')
experiment_name = full_name.pop()
experiment_group = full_name.pop() if len(full_name) > 0 else ''

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

with tf.Session(config=config) as sess:

    factory.restore_checkpoint(sess, tf.train.Saver(), ckpt_dir)

    R = [[0.38194239, -0.92415936, 0.0070394], [-0.88550567, -0.36812646, -0.283484], [0.26457555, 0.102041, -0.958951]]
    print(R)

    img = dataset.render_rot( R,downSample = 1)
    
    cv2.imshow('pred_view', cv2.resize(img,(256,256)))
    cv2.waitKey(0)


