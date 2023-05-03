## Augmented Autoencoders  

### Enviroment Installation
Please follow the instructions in this [repo](https://github.com/DLR-RM/AugmentedAutoencoder)

### Runing Commands
#### Setup enviroment
```bash
conda activate aae_py37_tf26

pip install .

export AE_WORKSPACE_PATH=/home/zjh/Desktop/AAE_pro/autoencoder_ws  

mkdir $AE_WORKSPACE_PATH
cd $AE_WORKSPACE_PATH
ae_init_workspace
cd ..
```

#### Training
```bash
./scripts/train.sh
```


#### Evaluation
Select Object:

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