from pymongo import MongoClient
from configs import Config
from flask import request

client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()
database_sensor = db["testing_sensor"]
database_users = db["users"]

def get_data():
    """Mengambil dan memproses data terbaru dari collection 'testing_sensor' di MongoDB."""
    data = database_sensor.find().sort('timestamp', -1)
    
    monitoring_data = []
    for idx, record in enumerate(data, start=1):
        monitoring_data.append({
            "no": idx,
            "timestamp": record['timestamp'],
            "ph": record['ph'],
            "temperature": f"{record['temperature']} Derajat",
            "tds": f"{record['tds']} PPM",
            "turbidity": f"{record['turbidity']} NTU",
            "water_quality": record['water_quality']
        })

    return monitoring_data  