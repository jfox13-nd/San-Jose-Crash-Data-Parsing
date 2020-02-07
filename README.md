# City of San Jose Traffic Crash Data Parsing

DOT Report 39 is document (that may soon be made publically available) containing all recorded traffic crash data for the city of San Jose, starting from the 70s.

This repo provides basic Report 39 parsing and data cleaning scripts for use by the public. It will soon have scripts that will estimate the lattitude and longitude of each crash where this information is not available.

## Explanation of the data

Report 39 is a CSV that contains the following information on every collision incident:
- Int #: Intersection Number
- IntersectionName
- TcrNumber: A unique ID for each crash
- CrashDateTime
- Direction From Intersection
- Distance
- ProximityToIntersection
- Weather
- Lighting
- RoadwaySurface
- VehicleInvolvedWith
- CollisionType
- FatalInjuries
- SevereInjuries
- ModerateInjuries
- MinorInjuries
- PrimaryCollisionFactor

It also has the following information available for every involved party in a collision
- Sex
- Age
- PartyType
- MovementPrecedingCollision
- VehicleDirection
- ViolationCodeDescription

Of note is that the city of San Jose did not record the GPS coordinates of crashes until a few years ago. GPS data is not available in Report 39, although the closest intersection, distance to that intersection, and cardinal direction (of the crash in reference to the intersection) are found in report 39. From this the GPS coordinate of a crash can be extrapolated.

The following is a sample .json output of clean.py:
```
{
    "10-174-0012": {
        "Int #": "1055",
        "IntersectionName": "ABBEY LN & BUCKNALL RD",
        "CrashDateTime": "6/23/2010 0:15",
        "DirectionFromIntersection": "West Of",
        "Distance": 0,
        "ProximityToIntersection": "Related",
        "Weather": "Clear",
        "Lighting": "Dark - Street Light",
        "RoadwaySurface": "Dry",
        "VehicleInvolvedWith": "Parked Vehicle",
        "CollisionType": "Other",
        "FatalInjuries": 0,
        "SevereInjuries": 0,
        "ModerateInjuries": 0,
        "MinorInjuries": 0,
        "PrimaryCollisionFactor": "Violation Driver 1",
        "Parties": [
            {
                "Sex": null,
                "Age": "0",
                "PartyType": "Panel Truck",
                "MovementPrecedingCollision": "Parked",
                "VehicleDirection": "East",
                "ViolationCodeDescription": "Unknown"
            },
            {
                "Sex": null,
                "Age": null,
                "PartyType": null,
                "MovementPrecedingCollision": null,
                "VehicleDirection": "West",
                "ViolationCodeDescription": "Unknown"
            },
            {
                "Sex": "M",
                "Age": "52",
                "PartyType": "Car",
                "MovementPrecedingCollision": "Proceeding Straight",
                "VehicleDirection": "West",
                "ViolationCodeDescription": "Driving Drunk"
            }
        ]
    },
}
```

The following information should be included in a file named .secret
```
GOOGLE_API_KEY
```

## Description of files

### clean.py
Takes a Report 39 csv cleans the data and converts to a JSON file.

### find_coords.py
[TODO] Script that takes in the clean Report 39 JSON file finds the GPS locations of each collision and creates a new JSON file with this additional information.

### osm.py
[TODO] Given a street name and a corresponding gps coordinate on that street find all the gps coordinates on that road
This script is mainly for testing, its content will eventually be incorporated into other scripts or made a module.