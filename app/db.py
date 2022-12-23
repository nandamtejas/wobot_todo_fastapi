from pymongo import MongoClient
import certifi
from .config import MONGO_URI

client = MongoClient(MONGO_URI, tlsCAfile=certifi.where())
db = client.get_database("wobot")