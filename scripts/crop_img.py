import argparse
import json
import os
import cv2
import re

def read_json_file(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return data

def crop_images(data, image_folder, output_folder, padding=10):
    for scene_num, scene_data in data.items():
        img_name = f"{int(scene_num):06d}.png"
        img_path = os.path.join(image_folder, img_name)

        if os.path.exists(img_path):
            img = cv2.imread(img_path)
            img_height, img_width, _ = img.shape

            for i, bbox in enumerate(scene_data["bbox_obj"]):
                x, y, w, h = bbox
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = min(w + 2 * padding, img_width - x)
                h = min(h + 2 * padding, img_height - y)

                cropped_img = img[y:y+h, x:x+w]

                # Save the cropped image
                # output_dir = os.path.join(output_folder, "roi")
                # if not os.path.exists(output_dir):
                #     os.makedirs(output_dir)

                output_img_path = os.path.join(output_folder, f"{img_name[:-4]}.png")
                cv2.imwrite(output_img_path, cropped_img)

def main(json_file, image_folder):
    data = read_json_file(json_file)

    number = int(re.search(r"(\d+)_roi\.json", args.json_file).group(1))

    base_dir = os.path.dirname(args.json_file)
    folder_dir = os.path.join(base_dir, f"{number}_roi")
    os.makedirs(folder_dir, exist_ok=True)
    
    crop_images(data, image_folder, folder_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", help="Path to the crop_roi.json file")
    parser.add_argument("image_folder", help="Path to the image folder")
    args = parser.parse_args()

    main(args.json_file, args.image_folder)
