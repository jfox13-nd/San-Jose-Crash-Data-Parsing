#!/usr/bin/env python3

'''clean.py: script for cleaning DOT report 39 data'''
__author__ = "Jack Fox"
__email__ = "jfox13@nd.edu"

import csv
import json

r39_csv_name = "r39.csv"
r39_formatted_csv_name = "r39_formatted.csv"
r39_json_name = "r39.json"


def generate_formatted_csv(r39_csv=r39_original_csv_name, r39_csv_formatted=formatted_csv_name) -> None:
    '''removes irrelevant lines from top of r39.csv'''
    # reads from original csv, removes top lines
    with open(r39_csv, 'r') as f:
        r39_contents = f.readlines()
        csv_start_line = 0
        while "Int #" not in r39_contents[csv_start_line]:
            csv_start_line += 1
        r39_contents = r39_contents[csv_start_line:]
    r39_contents = [ line.strip() for line in r39_contents ]
    
    with open(r39_csv_formatted, 'w') as f:
        for line in r39_contents:
            f.write("{}\n".format(line))

def csv_to_json(r39_csv=formatted_csv_name, r39_json=r39_json_name):
    '''converts r39 formatted csv to a json object'''
    with open(r39_csv, 'r') as f:
        csvReader = csv.DictReader(r39_csv)

if __name__ == '__main__':
    #generate_formatted_csv()
    csv_to_json()