import os
import json
import argparse

def extract_cam_R_m2c(json_file_path, obj_id):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    result = {}
    for scene_num, objects in data.items():
        for obj in objects:
            if obj["obj_id"] == obj_id:
                result[scene_num] = obj["cam_R_m2c"]

    return result

def save_to_json(result, output_file):
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file_path", help="Path to the JSON file")
    parser.add_argument("obj_id", type=int, help="Object ID to search for")
    args = parser.parse_args()
    parent_folder = os.path.dirname(args.json_file_path)
    # print(parent_folder)
    result = extract_cam_R_m2c(args.json_file_path, args.obj_id)
    output_file = f"{parent_folder}/{args.obj_id}_gt.json"
    save_to_json(result, output_file)

# import json

# def extract_cam_R_m2c(json_file_path, obj_id):
#     with open(json_file_path, 'r') as f:
#         data = json.load(f)

#     result = {}
#     for scene_num, objects in data.items():
#         for obj in objects:
#             if obj["obj_id"] == obj_id:
#                 result[scene_num] = obj["cam_R_m2c"]

#     return result

# def save_to_json(result, output_file):
#     with open(output_file, 'w') as f:
#         json.dump(result, f, indent=2)

# if __name__ == "__main__":
#     json_file_path = "000001/scene_gt.json" # Replace this with the path to your JSON file
#     obj_id = 2

#     result = extract_cam_R_m2c(json_file_path, obj_id)
#     output_file = f"000001/{obj_id}_gt.json"
#     save_to_json(result, output_file)
