#!/usr/bin/env python3

'''
osm.py: given a street name and a corresponding gps coordinate on that street find all the gps coordinates on that road
This script is mainly for testing, its content will eventually be incorporated into other scripts or made a module
'''
__author__ = "Jack Fox"
__email__ = "jfox13@nd.edu"

import requests
import json
import pprint
import re

from find_coords import lat_adjust, lng_adjust

overpass_url = "http://overpass-api.de/api/interpreter"
osm_node_url = "https://api.openstreetmap.org/api/0.6/node/"
# km
bound_radius = 0.1

def osm_query(lat, lng):
    north_bound = lat_adjust(lat,bound_radius)
    south_bound = lat_adjust(lat, -1 * bound_radius)
    east_bound = lng_adjust(lat,lng,bound_radius)
    west_bound = lng_adjust(lat,lng, -1 * bound_radius)

    q1 = """
    [bbox:{},{},{},{}]
    [out:json];
    (way[highway];);
    out center;
    """.format(south_bound,west_bound,north_bound,east_bound)
    
    response = requests.get(overpass_url, 
                            params={'data': q1})
    data = response.json()
    pprint.pprint(data)
    '''
    for elem in data['elements']:
        #pprint.pprint(elem)
        print(get_node_lat_lng(elem['nodes'][0]))
        break
    '''

def get_node_lat_lng(node: str) -> tuple:
    node_url = '{}{}'.format(osm_node_url,node)
    res = requests.get(node_url)
    data = res.text
    lon_search = re.search('lon="([^"]*)"',data)
    lat_search = re.search('lat="([^"]*)"',data)
    print(data)
    if lon_search and lat_search:
        return float(lat_search.group(1)), float(lon_search.group(1))
    else:
        return None, None


if __name__ == '__main__':
    # for bailey ave, every road within 1km
    osm_query(37.209986,-121.722075)