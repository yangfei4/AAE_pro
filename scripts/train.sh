#!/bin/bash

# List of object names
objects=(
"obj_01.ply"
)

# Base path
AE_WORKSPACE_PATH="./autoencoder_ws"

# Loop through object names
for obj_name in "${objects[@]}"; do
    # Create the directory
    obj_dir="${AE_WORKSPACE_PATH}/cfg/exp_group_${obj_name%.*}"
    mkdir -p "$obj_dir"

    # Copy the train_template.cfg to the new directory
    cp "${AE_WORKSPACE_PATH}/cfg/train_template.cfg" "${obj_dir}/my_autoencoder.cfg"

    pre_obj_path="/home/zjh/Desktop/AAE_pro/data/tless_models/${obj_name}"
    # Replace the path = ... line with the obj_name
    sed -i "s|^MODEL_PATH: .*|MODEL_PATH: ${pre_obj_path}|" "${obj_dir}/my_autoencoder.cfg"

    # Run your command or script that uses the modified my_autoencoder.cfg here
    # For example:
    # ./your_script.sh "${obj_dir}/my_autoencoder.cfg"
    ae_train "exp_group_${obj_name%.*}"/my_autoencoder
    # Sleep between iterations, if needed (optional, remove or adjust as needed)
    sleep 1
done
