## Augmented Autoencoders  

![results](./visual/aae_res/combined_image_vertical.png)

### Enviroment Installation
You can create and install required packages with conda.

```bash
conda env create -f aae.yml
```

### Runing Commands

1. Activate conda environment.
   ```bash
   conda activate aae
   ```
2. `cd` to the root directory of this project, then run
   ```bash
   pip install .
   ```
3. Set up the workspace path, for example:
   ```bash
   export AE_WORKSPACE_PATH=/home/zjh/Desktop/autoencoder_ws  
   ```
4. Run the following commands to initialize the workspace.
   ```bash
   mkdir $AE_WORKSPACE_PATH
   cd $AE_WORKSPACE_PATH
   ae_init_workspace
   ```

#### Training
1. There's a training script in the `scripts` directory. Before you run it directly, you need to down the training data:
   ```bash
   ./scripts/download_data.sh
   ```

2. Then replace `BACKGROUND_IMAGES_GLOB` in `$AE_WORKSPACE_PATH/cfg/train_template.cfg` with the downloaded VOC dataset path.

3. Finally, you can run the training script:

    ```bash
    ./scripts/train.sh
    ```
    You can adjust the object numbers to be trained and the object path in the `train.sh`.

### Evaluation
We selected 10 objects from the T-LESS dataset for evaluation. They vary in shape, size and symmetric properties. The objects are numbered as follows:

```bash
Selected Objects:

- 01 (trained, evalued in folder 000005, idx 0)
- 02 (trained, evalued in folder 000001, idx 0)
# - 04 (trained, replaced by 05)
- 05 (trained, evaluating in folder 000002, idx 0)
- 12 (trained, evalued in folder 000003, idx 3)
- 14 (trained, evalued in folder 000007, idx 3)
- 15 (trained, evalued in folder 000007, idx 4)
- 16 (trained, evalued in folder 000007, idx 5)
- 18 (trained, evalued in folder 000003, idx 4)
- 27 (trained, evalued in folder 000015, idx 2)
- 29 (trained, evalued in folder 000015, idx 4)
```

#### Create Test Images
##### 1. Render Ground Truth from Pose Information
- `data/t_less/t-less_v2/test_primesense` contains 20 folders having ground truth in different scenes. Each scene may have 2-3 objects from T-Less. Take `000001` for example,  `scene_gt.json` contains obj id and its rotation matrix.
   
  To parse the `.json` file, getting a json called `{object_id}_gt.json` only for one object, run: 

  ```shell
  python ./scripts/filter.py path_to_json_file object_id
  ```
  e.g.
  ```shell 
  python ./scripts/filter.py data/t_less/t-less_v2/test_primesense/000001/scene_gt.json 25
  ```

- Render the corresponding image using extracted pose information

  ```shell
  python ./scripts/save_gt.py path_to_{object_id}_gt.json exp_name
  ```
  e.g.
  ```shell
  python ./scripts/save_gt.py ./data/t_less/t-less_v2/test_primesense/000001/2_gt.json exp_group_obj_15/my_autoencoder
  ```

##### 2. Generate Cropped Test Images
-  Parse `scene_gt_info.json` to get the object's bounding box, it will generate a `{object_id}_roi.json` file containing bbox location, where index_id is the order of the target object in the `scene_gt_info.json`.
   
   ```shell
   python ./scripts/extract_crop_bbx.py --obj_id=<obj_id> --index=<index_th> path_to_scene_gt_info.json
   ```
   e.g.
   ```shell
   python ./scripts/extract_crop_bbx.py --obj_id=2 --index=0 ./data/t_less/t-less_v2/test_primesense/000001/scene_gt_info.json
   ```
- Generate cropped test images using
  ```shell
  python ./scripts/crop_img.py path_to_{object_id}_roi.json path_to_image_folder
  ```
  e.g.
  ```shell
  python ./scripts/crop_img.py ./data/t_less/t-less_v2/test_primesense/000001/2_roi.json ./data/t_less/t-less_v2/test_primesense/000001/rgb
  ```
After the above operations, we'll get our test image folder `{obj_id}_roi` and ground truth image folder `{obj_id}_gt`. The test images will be fed into a trained AAE model to get predicted poses.

##### 3. Render Predicted Pose
   ```shell
   python auto_pose/test/aae_image.py exp_group_obj_15/my_autoencoder -f /home/zjh/Desktop/AAE_pro/data/t_less/t-less_v2/test_primesense/000001/2_roi   
   ```

##### 4. Compare these two images using mAP and mAR metrics.
Evaluation [code](./evaluate.ipynb)
- Image mertrics
  Convert rgb image to binary image
- Computer mAP & mAR @IoU0.75
- Computer average Euler angle error for each axis [roll, pitch, yaw]



### Reference: 
This project is a re-implementation of [DLR-RM/AugmentedAutoencoder](https://github.com/DLR-RM/AugmentedAutoencoder).