#!/usr/bin/env python3

'''clean.py: script for cleaning DOT report 39 data'''
__author__ = "Jack Fox"
__email__ = "jfox13@nd.edu"

import json
import pprint

r39_original_csv_name = "r39.csv"
r39_json_name = "r39.json"


def generate_formatted_csv_data(r39_csv: str = r39_original_csv_name) -> list:
    '''
    generates list of relevant data from Report 39 csv
    
    The following assumptions are made about the given data
    * entries with an index (Int #) listed as '(blank)' are to be excluded from the data
    '''
    # reads from original csv, removes header and converts to list
    with open(r39_csv, 'r') as f:
        r39_contents = f.readlines()
        csv_start_line = 0
        while "Int #" not in r39_contents[csv_start_line]:
            csv_start_line += 1
        r39_contents = r39_contents[csv_start_line:]
    r39_contents = [ line.strip() for line in r39_contents ]
    
    # removes invalid data
    r39_contents_formatted = []
    for line in r39_contents:
        if line.startswith("(blank)") or line.startswith("Grand Total"):
            continue
        r39_contents_formatted.append(line)
    
    return r39_contents_formatted

def csv_to_json(r39_csv_data: list, r39_json_file: str = r39_json_name) -> None:
    '''converts r39 formatted csv to a json object'''
    r39_dict = {}

    header = r39_csv_data[0].split(',')
    r39_csv_data = r39_csv_data[1:]

    numberical_columns = [
                'Distance',
                'FatalInjuries',
                'SevereInjuries',
                'ModerateInjuries',
                'MinorInjuries'
            ]
    last_index = 0
    
    for line in r39_csv_data:
        line = line.split(',')
        # standardizes how null entries are represented in the data
        for index, column in enumerate(line):
            if column == 'None' or column == '(blank)' or column == '':
                line[index] = None
        
        if line[0]:
            int_index = int(line[0])
            last_index = int_index
            r39_dict[int_index] = {
                'IntersectionName':line[1],
                'TcrNumber':line[2],
                'CrashDateTime':line[3],
                'DirectionFromIntersection':line[4],
                'Distance':line[5],
                'ProximityToIntersection':line[6],
                'Weather':line[7],
                'Lighting':line[8],
                'RoadwaySurface':line[9],
                'VehicleInvolvedWith':line[10],
                'CollisionType':line[11],
                'FatalInjuries':line[12],
                'SevereInjuries':line[13],
                'ModerateInjuries':line[14],
                'MinorInjuries':line[15],
                'PrimaryCollisionFactor':line[16],
                'Parties': list()
            }
            for column in numberical_columns:
                if r39_dict[int_index][column]:
                    r39_dict[int_index][column] = int(r39_dict[int_index][column])
                        
        else:
            int_index = last_index

        party = dict()

        party['Sex'] = line[17]
        party['Age'] = line[18]
        party['PartyType'] = line[19]
        party['MovementPrecedingCollision'] = line[20]
        party['VehicleDirection'] = line[21]
        party['ViolationCodeDescription'] = line[22]

        r39_dict[int_index]['Parties'].append(party)

    with open(r39_json_file,'w+') as f:
        f.write(json.dumps(r39_dict,indent=4))
        
        
if __name__ == '__main__':
    csv_to_json(generate_formatted_csv_data())
