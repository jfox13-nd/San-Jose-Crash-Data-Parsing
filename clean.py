#!/usr/bin/env python3

'''clean.py: script for cleaning DOT report 39 data'''
__author__ = "Jack Fox"
__email__ = "jfox13@nd.edu"

import json

r39_original_csv_name = "r39_full.csv"
r39_json_name = "r39_full.json"


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

    numerical_columns = [
                'Distance',
                'FatalInjuries',
                'SevereInjuries',
                'ModerateInjuries',
                'MinorInjuries'
            ]
    last_index = ''
    last_int_num = ''
    last_int_name = ''
    
    for line in r39_csv_data:
        line = line.split(',')
        # standardizes how null entries are represented in the data
        for index, column in enumerate(line):
            if column == 'None' or column == '(blank)' or column == '':
                line[index] = None
        
        if line[2]:
            tcr_number = line[2]
            last_index = tcr_number
            r39_dict[tcr_number] = {
                'Int #': line[0],
                'IntersectionName':line[1],
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

            if not line[0] and not line[1]:
                r39_dict[tcr_number]['Int #'] = last_int_num
                r39_dict[tcr_number]['IntersectionName'] = last_int_name
            else:
                last_int_num = r39_dict[tcr_number]['Int #']
                last_int_name = r39_dict[tcr_number]['IntersectionName']

            for column in numerical_columns:
                if r39_dict[tcr_number][column]:
                    r39_dict[tcr_number][column] = int(r39_dict[tcr_number][column])
                        
        else:
            tcr_number = last_index

        party = dict()

        party['Sex'] = line[17]
        party['Age'] = line[18]
        party['PartyType'] = line[19]
        party['MovementPrecedingCollision'] = line[20]
        party['VehicleDirection'] = line[21]
        party['ViolationCodeDescription'] = line[22]

        r39_dict[tcr_number]['Parties'].append(party)

    with open(r39_json_file,'w+') as f:
        f.write(json.dumps(r39_dict,indent=4))
        
        
if __name__ == '__main__':
    csv_to_json(generate_formatted_csv_data())
