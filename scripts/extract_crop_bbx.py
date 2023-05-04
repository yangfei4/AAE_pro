import json
import argparse
import os
import re

def read_json_file(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return data

def extract_index_entry(data, index):
    result = {}
    for scene_num, objects in data.items():
        if index < len(objects):
            if scene_num not in result:
                result[scene_num] = {"bbox_obj": []}
            result[scene_num]["bbox_obj"].append(objects[index]['bbox_obj'])
    return result

def save_to_json(result, output_file):
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

def main(index, input_json_file):
    data = read_json_file(input_json_file)
    extracted_data = extract_index_entry(data, index)
    
    output_file = os.path.join(os.path.dirname(input_json_file), f"{args.obj_id}_roi.json")
    save_to_json(extracted_data, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--obj_id", type=int, help="id of object")
    parser.add_argument("--index", type=int, help="Index of the entry to extract")
    parser.add_argument("input_json_file", help="Path to the input JSON file")
    args = parser.parse_args()
    

    main(args.index, args.input_json_file)