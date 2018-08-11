from requests_futures.sessions import FuturesSession
import pymongo
from pymongo import MongoClient
from db_connector import get_mongo_client

client = get_mongo_client()
db = client.carChain
