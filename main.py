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
import time

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

correct_plates = {
    '1': 'TST-0001',
    '2': 'TST-0002',
    '3': 'TST-0003',
    '4': 'TST-0004',
    '5': 'TST-0005'
}

jsons = []

for plate, trips in to_save.items():
    for meters, timestamp in trips:
        jsons.append({
            'timestamp': timestamp,
            'carPlate': correct_plates[plate],
            'block': {
                'data': meters
            }
        })

# TODO: juntar total por dia pra mandar

for obj in jsons:
    r = requests.post(endpoint, json=obj)
    print(r.status_code)
    pprint(json.loads(r.content))
    time.sleep(2)

# with FuturesSession(max_workers=20) as session:
#     futures = []
#     for obj in jsons:
#         futures.append(session.post(endpoint, json=obj))      # TODO: this should be updated when a final request type is defined

#     for future in futures:
#         pprint(future.result())     # result from the request, should have information about the acceptance of the block
