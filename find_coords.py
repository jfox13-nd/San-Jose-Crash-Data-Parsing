#!/usr/bin/env python3

'''clean.py: script for cleaning DOT report 39 data'''
__author__ = "Jack Fox"
__email__ = "jfox13@nd.edu"

import json
import pprint
import geopandas
import geopy
import pandas
import requests
import re
import certifi
import urllib
import math

r39_json_name = "r39.json"
r39_json_name_coords = "r39_coords.json"
# radius of earth in km
radius_earth = 6371.0

with open('.secret','r') as secret_file:
    API_KEY = secret_file.readlines()[0].strip()
    

def generate_coords_file(original_file: str = r39_json_name, output_file: str = r39_json_name_coords) -> None:
    ''' creates a JSON file with GPS data included '''
    with open(original_file, 'r') as f:
        r39_dict = json.load(f)

    for entry in r39_dict:
        r39_dict[entry]['lattitude'], r39_dict[entry]['longitude'] = find_gps_coordinates(r39_dict[entry])
        break

    '''
    with open(output_file,'w+') as f:
        f.write(json.dumps(r39_dict,indent=4))
    '''

    
def find_gps_coordinates(collision: dict) -> tuple:
    '''
    finds the GPS coordinates of a given collision

    assumptions about the data:
    * If no distance or direction is available then the intersection position is returned
    * If no direction is available then the intersection point is returned
    * If the location of an intersection cannot be found then (None, None) is returned
    '''
    addr = collision["IntersectionName"]
    distance = collision["Distance"]

    # convert feet to km
    if distance:
        distance *= 0.3048

    intersection_res = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(addr,API_KEY))
    if not intersection_res['results'] or not intersection_res['results'][0] or not intersection_res['results'][0]['geometry'] or not intersection_res['results'][0]['geometry']['location']:
        print("Failed to get gps coordinates of crash at {}".format(addr))
        return None,None

    intersection_lat = intersection_res['results'][0]['geometry']['location']['lat']
    intersection_lng = intersection_res['results'][0]['geometry']['location']['lng']

    if not distance:
        return intersection_lat, intersection_lng
    real_lat = intersection_lat
    real_lng = intersection_lng

    
    
    return real_lat,real_lng

def uo(args, **kwargs):
    return urllib.request.urlopen(args, cafile=certifi.where(), **kwargs)

def lat_adjust(lat: float, km: float) -> float:
    ''' returns adjusted lattitude, positive km argument for North, negative for South '''
    return lat + (km / radius_earth) * (180.0 / math.pi)

def lng_adjust(lat: float, lng: float, km: float) -> float:
    ''' returns adjusted lattitude, positive km argument for East, negative for West '''
    return lng + (km / radius_earth) * (180.0 / math.pi) / math.cos(lat * math.pi / 180.0)

if __name__ == '__main__':
    generate_coords_file()