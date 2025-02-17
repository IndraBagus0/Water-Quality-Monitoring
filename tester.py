from pymongo import MongoClient
from datetime import datetime
import pytz  # Import untuk timezone Jakarta
import random
import time

# Koneksi ke MongoDB
client = MongoClient("mongodb+srv://indra:nnBigGhtZnZizObM@hostdb.vbod5.mongodb.net/?retryWrites=true&w=majority&appName=HostDB")
db = client["water_quality"]
collection = db["testing_sensor"]

jakarta_tz = pytz.timezone("Asia/Jakarta")

try:
    # Looping hingga 100 kali
    for _ in range(100):
        # Ambil waktu saat ini dalam zona waktu Jakarta
        timestamp = datetime.now(jakarta_tz).strftime('%Y-%m-%d %H:%M:%S')

        # Simulasi data sensor dengan nilai acak
        sensor_data = {
            "timestamp": timestamp,
            "ph": round(random.uniform(6.5, 8.5), 2),
            "temperature": round(random.uniform(20, 30), 2),
            "tds": round(random.uniform(100, 500), 2),
            "turbidity": round(random.uniform(0, 5), 2),
            "water_quality": random.choice(["Layak", "Tidak Layak"])
        }

        # Menyimpan data ke database
        collection.insert_one(sensor_data)
        print(f"Data disimpan: {sensor_data}")

        # Tunggu 2 detik sebelum membaca data lagi
        time.sleep(2)

except KeyboardInterrupt:
    print("\nProgram dihentikan oleh pengguna.")
