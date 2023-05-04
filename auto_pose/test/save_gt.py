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
import argparse

from auto_pose.ae import factory, utils



def read_json_file(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return data

def convert_to_numpy_arrays(data):
    numpy_data = {}
    for scene_num, matrix in data.items():
        numpy_data[scene_num] = np.reshape(matrix, (3, 3))
    return numpy_data

def print_numpy_arrays_and_scenes(numpy_data):
    for scene_num, matrix in numpy_data.items():
        print(f"Scene: {scene_num}\nMatrix:\n{matrix}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target_json_file", help="Path to the target JSON file")
    parser.add_argument("experiment_name", help="Name of the experiment")
    args = parser.parse_args()

    data = read_json_file(args.target_json_file)
    numpy_data = convert_to_numpy_arrays(data)
    print_numpy_arrays_and_scenes(numpy_data)

    full_name = args.experiment_name.split('/')
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

    for img_id, R in numpy_data.items():
        with tf.Session(config=config) as sess:
            factory.restore_checkpoint(sess, tf.train.Saver(), ckpt_dir)

            print(R)

            img = dataset.render_rot( R,downSample = 1)
            base_dir = os.path.dirname(args.target_json_file)
            img_path = os.path.join(base_dir, "gt", f"{img_id}.png")
            cv2.imwrite(img_path, img)

            # cv2.imshow('pred_view', cv2.resize(img,(256,256)))
            # cv2.waitKey(0)