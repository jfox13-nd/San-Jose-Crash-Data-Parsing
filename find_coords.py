#!/usr/bin/env python3

'''find_coords.py: script for adding gps coordinates to report 39 data'''
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
import pprint
import sys

r39_json_name = "r39.json"
r39_json_name_coords = "r39_coords.json"
# radius of earth in km
radius_earth = 6371.0
# feet
gps_accuracy = 50
api_call_limit = 5

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
    * If there is a failure to snap a point to a nearby road then (None, None) is returned
    '''
    addr = collision["IntersectionName"]
    distance = collision["Distance"]

    if distance:
        distance_km = feet_to_km(distance)

    intersection_res = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(addr,API_KEY))
    intersection_res = intersection_res.json
    if not intersection_res['results'] or not intersection_res['results'][0] or not intersection_res['results'][0]['geometry'] or not intersection_res['results'][0]['geometry']['location']:
        print("Failed to get gps coordinates of crash at {}".format(addr), file=sys.stderr)
        return None,None

    intersection_lat = intersection_res['results'][0]['geometry']['location']['lat']
    intersection_lng = intersection_res['results'][0]['geometry']['location']['lng']

    if not distance:
        return intersection_lat, intersection_lng
    prev_lat = intersection_lat
    prev_lng = intersection_lng
    current_lat = lat_adjust(prev_lat, distance_km)
    current_lng = lat_adjust(prev_lat, prev_lng, distance_km)
    
    snap_point(current_lat,current_lng)

    if not current_lat and not current_lng:
        return None, None

    return current_lat, current_lng

def lat_adjust(lat: float, km: float) -> float:
    ''' returns adjusted lattitude, positive km argument for North, negative for South '''
    return lat + (km / radius_earth) * (180.0 / math.pi)

def lng_adjust(lat: float, lng: float, km: float) -> float:
    ''' returns adjusted lattitude, positive km argument for East, negative for West '''
    return lng + (km / radius_earth) * (180.0 / math.pi) / math.cos(lat * math.pi / 180.0)

def feet_to_km(feet: float) -> float:
    return feet * 0.3048

def km_to_feet(km: float) -> float:
    return km / 0.3048

def distance_between(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    ''' calculates distance between two gps coordinates in feet '''
    return geopy.distance.distance( (lat1,lng1), (lat2,lng2) ).feet

def snap_point(lat: float, lng: float) -> tuple:
    ''' snap a gps point to the nearest road, find that gps point '''
    res = requests.get('https://roads.googleapis.com/v1/snapToRoads?path={},{}&key={}'.format(lat,lng,API_KEY))
    res = res.json
    try:
        return res['snappedPoints'][0]['location']['latitude'], res['snappedPoints'][0]['location']['longitude']
    except:
        print("Snap failed:")
        pprint.pprint(res)
        return None,None

if __name__ == '__main__':
    generate_coords_file()