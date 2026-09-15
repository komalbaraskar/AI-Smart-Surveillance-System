import os
from pymongo import MongoClient
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/surveillance"
)

client = MongoClient(MONGO_URI)

db = client["surveillance"]

logs = db["logs"]
people_count = db["people_count"]
users = db["users"]
alerts = db["alerts"]
cameras = db["cameras"]
zones = db["zones"]

def save_log(message):
    logs.insert_one({
        "message": message,
        "time": datetime.now()
    })

def save_alert(
    alert_type,
    severity,
    message,
    person_id=None,
    camera_id="CAM01",
    evidence=None
):
    alerts.insert_one({
        "type": alert_type,
        "severity": severity,
        "message": message,
        "person_id": person_id,
        "camera_id": camera_id,
        "status": "new",
        "time": datetime.now(),
        "evidence": evidence
    })
def save_count(count):
    people_count.insert_one({
        "count": count,
        "time": datetime.now()
    })

def create_user(username, password, role="security"):
    password_hash = generate_password_hash(password)

    users.insert_one({
        "username": username,
        "password": password_hash,
        "role": role
    })

def authenticate_user(username, password):
    user = users.find_one({
        "username": username
    })
    if user and check_password_hash(
        user["password"],
        password
    ):
        return user

    return None