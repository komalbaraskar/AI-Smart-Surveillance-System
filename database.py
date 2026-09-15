import os
from pymongo import MongoClient

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/surveillance"
)

client = MongoClient(MONGO_URI)

db = client["surveillance"]

logs = db["logs"]
people_count = db["people_count"]


def save_log(message):
    logs.insert_one({
        "message": message
    })


def save_count(count):
    people_count.insert_one({
        "count": count
    })