from requests_futures.sessions import FuturesSession
from coordinates import Coordinate
import pymongo
from pymongo import MongoClient
from db_connector import get_mongo_client
from functools import reduce
from pprint import pprint
from endpoint import endpoint
from datetime import datetime
import json
import requests

client = get_mongo_client()
db = client.carChain

cursor = db.raw_sim_data.find({})

to_save = {}
for document in cursor:
    plate = document['car_plate']
    if not plate in to_save:
        to_save[plate] = []

    trip = [(Coordinate.Get_coordinate_from_json(obj['location']), str(obj['time']).split('.')[0]) for obj in document['trip']]
    total_meters = [(round(Coordinate.Distance(trip[i-1][0], trip[i][0])), trip[i][1]) for i in range(1, len(trip))]
    to_save[plate].extend(total_meters)

jsons = []

for plate, trips in to_save.items():
    for meters, timestamp in trips:
        jsons.append({
            'timestamp': timestamp,
            'carPlate': plate,
            'block': {
                'data': meters
            }
        })

with FuturesSession(max_workers=1) as session:
    futures = []
    for obj in jsons:
        futures.append(session.post(endpoint, json=obj))      # TODO: this should be updated when a final request type is defined

    for future in futures:
        pprint(future.result())     # result from the request, should have information about the acceptance of the block
