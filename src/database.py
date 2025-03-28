from pymongo import MongoClient
from configs import Config
from flask import request
import base64
import secrets


client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()
database_sensor = db["testing_sensor"]
database_users = db["users"]
database_alat = db["alat"]

def save_api_key(device_id, location):
    """Menyimpan API key baru untuk perangkat IoT."""
    api_key = secrets.token_hex(16)
    database_alat.insert_one({
        "device_id": device_id,
        "api_key": api_key,
        "location": location
    })
    return api_key

def get_data():
    """Mengambil dan memproses 100 data terbaru dari collection 'testing_sensor' di MongoDB."""
    data = database_sensor.find().sort('timestamp', -1).limit(100)
    
    monitoring_data = []
    for idx, record in enumerate(data, start=1):
        monitoring_data.append({
            "no": idx,
            "timestamp": record['timestamp'],
            "location": record['location'],
            "ph": record['ph'],
            "temperature": f"{record['temperature']} Derajat",
            "tds": f"{record['tds']} PPM",
            "turbidity": f"{record['turbidity']} NTU",
            "kelayakan": record['kelayakan']
        })

    return monitoring_data  

# list admin
def admin_data():
    """Mengambil data admin dari collection 'users' di MongoDB."""
    data = database_users.find()
    
    data_admin = []
    for idx, record in enumerate(data, start=1):
        profile_pic_base64 = None
        if "profile_pic" in record and record["profile_pic"]:
            profile_pic_base64 = base64.b64encode(record["profile_pic"]).decode("utf-8")
        data_admin.append({
            "no": idx,
            "id": str(record['_id']), 
            "username": record.get('username', 'N/A'),
            "email": record.get('email', 'N/A'),
            "name": record.get('name', 'N/A'),
            "phone": record.get('phone', 'N/A'),
            "address": record.get('address', 'N/A'),
            "profile_pic": profile_pic_base64
        })

    return data_admin