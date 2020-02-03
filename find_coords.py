#!/usr/bin/env python3

'''clean.py: script for cleaning DOT report 39 data'''
__author__ = "Jack Fox"
__email__ = "jfox13@nd.edu"

import json
import pprint

r39_json_name = "r39.json"
r39_json_name_coords = "r39_coords.json"

def generate_coords_file(original_file: str = r39_json_name, output_file: str = r39_json_name_coords) -> None:
    with open(original_file, 'r') as f:
        r39_dict = json.load(f)

    for entry in r39_dict:
        lat_long = find_gps_coordinates(r39_dict[entry])
        r39_dict[entry]['lattitude'] = lat_long[0]
        r39_dict[entry]['longitude'] = lat_long[0]

    '''
    with open(output_file,'w+') as f:
        f.write(json.dumps(r39_dict,indent=4))
    '''
    
def find_gps_coordinates(collision: dict) -> tuple:
    return 0, 0


if __name__ == '__main__':
    generate_coords_file()