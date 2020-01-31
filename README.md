# City of San Jose Vehicle Crash Data Parsing

DOT Report 39 is a soon to be made publically avaible document containing all recorded traffic crash data for the city of San Jose, starting at around the 70s.

This repo provides basic Report 39 parsing and data cleaning scripts for use by the public. It will soon have scripts that will estimate the lattitude and longitude of each crash where this information is not available.

## Explanation of the data

Report 39 is a CSV that contains the following information on every collision incident:
- Int #: this is a index for each collision incident
- IntersectionName
- TcrNumber
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