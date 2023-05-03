## Augmented Autoencoders  

### Enviroment Installation
You can create and install required packages with conda.

```bash
conda env create -f aae_py37_tf26.yml
```

Reference: [DLR-RM/AugmentedAutoencoder](https://github.com/DLR-RM/AugmentedAutoencoder)

### Runing Commands

1. Activate conda environment.
   ```bash
   conda activate aae_py37_tf26
   ```
2. `cd` to the root directory of this project, then run
   ```bash
   pip install .
   ```
3. Set up the workspace path, for example:
   ```bash
   export AE_WORKSPACE_PATH=/home/zjh/AAE_pro/autoencoder_ws  
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

#### Evaluation
We selected 10 objects from the T-LESS dataset for evaluation. They vary in shape, size and symmetric properties. The objects are numbered as follows:

```bash
Selected Object:

- 01
- 02 (trained)
- 04
- 12 (trained)
- 14
- 15
- 16
- 18 (trained)
- 27
- 29