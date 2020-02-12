#!/usr/bin/env python3

'''
analysis.py: provides basic functionality to perform some analysis of crash data
'''
__author__ = "Jack Fox"
__email__ = "jfox13@nd.edu"

import json
import pprint

crash_json = 'r39_full.json'


def analyze_dict(d: dict) -> None:
    ''' provide a readable analysis of a dictionary of crash information '''
    print("Number of collisions: {}".format(len(d)))
    print("Number of unique intersections: {}".format(len(unique_intersections(d))))
    print("Number of collisions for which a crash location can be extrapolated: {}".format(usable_collisions(d)))


def unique_intersections(d: dict) -> set:
    ''' produce a set of all unique intersections in the data '''
    intersections = set()

    for crash in d:
        intersections.add(d[crash]['Int #'])
    return intersections

def usable_collisions(d: dict) -> int:
    ''' returns a count of the number of collisions on which a crash location can be extrapolated '''
    count = 0

    for crash in d:
        if d[crash]['Int #'] is not None and d[crash]['IntersectionName'] is not None and d[crash]['DirectionFromIntersection'] is not None and d[crash]['Distance'] is not None:
            count += 1
    return count

if __name__ == '__main__':
    with open(crash_json, 'r') as f:
        analyze_dict(json.load(f))
