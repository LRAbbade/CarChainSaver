from requests_futures.sessions import FuturesSession
from coordinates import Coordinate
import pymongo
from pymongo import MongoClient
from db_connector import get_mongo_client
from functools import reduce
from pprint import pprint
from endpoint_ip import endpoint_ip

client = get_mongo_client()
db = client.carChain

query = {
    "saved_in_blockchain" : {
        "$exists" : False
    }
}

cursor = db.raw_sim_data.find(query)

to_save = {}
for document in cursor:
    plate = document['car_plate']
    if not plate in to_save:
        to_save[plate] = []

    trip = [Coordinate.Get_coordinate_from_json(obj['location']) for obj in document['trip']]
    total_meters = [Coordinate.Distance(trip[i-1], trip[i]) for i in range(1, len(trip))]
    to_save[plate].append(total_meters)

jsons = [{'car_plate':plate, 'data':trips} for plate, trips in to_save.items()]
pprint(jsons)   # for testing purposes

# with FuturesSession(max_workers=5) as session:
#     futures = []
#     for json in jsons:
#         futures.append(session.post(endpoint_ip, json))      # TODO: this should be updated when a final request type is defined
#
#     for future in futures:
#         pprint(future.result())     # result from the request, should have information about the acceptance of the block
