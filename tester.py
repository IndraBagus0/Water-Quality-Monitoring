class FuzzySet:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def membership(self, x):
        if x <= self.a or x >= self.d:
            return 0
        elif self.b <= x <= self.c:
            return 1
        elif self.a < x < self.b:
            return (x - self.a) / (self.b - self.a)
        else:
            return (self.d - x) / (self.d - self.c)


# Definisi Fuzzy Set
asam = FuzzySet(0, 0, 5, 7)
netral = FuzzySet(6.5, 7, 8, 8.5)
basa = FuzzySet(8, 9, 14, 14)

baik = FuzzySet(0, 0, 200, 500)
cukup = FuzzySet(300, 500, 700, 1000)
tidak_baik = FuzzySet(900, 1000, 1000, 1000)

jernih = FuzzySet(0, 0, 2, 5)
cukup_jernih = FuzzySet(4, 10, 15, 25)
keruh = FuzzySet(24, 25, 2000, 2000)

def defuzzify_sugeno(numerator, denominator):
    return 0 if denominator == 0 else numerator / denominator

def fuzzy_logic(input_pH, input_TDS, input_Kekeruhan):
    
    
    rules = [
        (asam.membership(input_pH), baik.membership(input_TDS), jernih.membership(input_Kekeruhan), 50),
        (asam.membership(input_pH), baik.membership(input_TDS), cukup_jernih.membership(input_Kekeruhan), 50),
        (asam.membership(input_pH), baik.membership(input_TDS), keruh.membership(input_Kekeruhan), 50),
        (asam.membership(input_pH), cukup.membership(input_TDS), jernih.membership(input_Kekeruhan), 50),
        (asam.membership(input_pH), cukup.membership(input_TDS), cukup_jernih.membership(input_Kekeruhan), 50),
        (asam.membership(input_pH), cukup.membership(input_TDS), keruh.membership(input_Kekeruhan), 50),
        (asam.membership(input_pH), tidak_baik.membership(input_TDS), jernih.membership(input_Kekeruhan), 50),
        (asam.membership(input_pH), tidak_baik.membership(input_TDS), cukup_jernih.membership(input_Kekeruhan), 50),
        (asam.membership(input_pH), tidak_baik.membership(input_TDS), keruh.membership(input_Kekeruhan), 50),

        (netral.membership(input_pH), baik.membership(input_TDS), jernih.membership(input_Kekeruhan), 100),
        (netral.membership(input_pH), baik.membership(input_TDS), cukup_jernih.membership(input_Kekeruhan), 100),
        (netral.membership(input_pH), baik.membership(input_TDS), keruh.membership(input_Kekeruhan), 50),
        (netral.membership(input_pH), cukup.membership(input_TDS), jernih.membership(input_Kekeruhan), 100),
        (netral.membership(input_pH), cukup.membership(input_TDS), cukup_jernih.membership(input_Kekeruhan), 100),
        (netral.membership(input_pH), cukup.membership(input_TDS), keruh.membership(input_Kekeruhan), 50),
        (netral.membership(input_pH), tidak_baik.membership(input_TDS), jernih.membership(input_Kekeruhan), 50),
        (netral.membership(input_pH), tidak_baik.membership(input_TDS), cukup_jernih.membership(input_Kekeruhan), 50),
        (netral.membership(input_pH), tidak_baik.membership(input_TDS), keruh.membership(input_Kekeruhan), 50),
       
        (basa.membership(input_pH), baik.membership(input_TDS), jernih.membership(input_Kekeruhan), 50),
        (basa.membership(input_pH), baik.membership(input_TDS), cukup_jernih.membership(input_Kekeruhan), 50),
        (basa.membership(input_pH), baik.membership(input_TDS), keruh.membership(input_Kekeruhan), 50),
        (basa.membership(input_pH), cukup.membership(input_TDS), jernih.membership(input_Kekeruhan), 50),
        (basa.membership(input_pH), cukup.membership(input_TDS), cukup_jernih.membership(input_Kekeruhan), 50),
        (basa.membership(input_pH), cukup.membership(input_TDS), keruh.membership(input_Kekeruhan), 50),
        (basa.membership(input_pH), tidak_baik.membership(input_TDS), jernih.membership(input_Kekeruhan), 50),
        (basa.membership(input_pH), tidak_baik.membership(input_TDS), cukup_jernih.membership(input_Kekeruhan), 50),
        (basa.membership(input_pH), tidak_baik.membership(input_TDS), keruh.membership(input_Kekeruhan), 50),
    ]

    numerator = 0
    denominator = 0

    for rule in rules:
        weight = rule[0] * rule[1] * rule[2]  # Perhitungan bobot fuzzy
        numerator += weight * rule[3]
        denominator += weight

    return defuzzify_sugeno(numerator, denominator)


# Contoh Input Sensor
suhu = 25.62
pH = 6.84
TDS = 20.51
turbidity = 1

# Hitung fuzzy logic
kelayakan_air = fuzzy_logic(pH, TDS, turbidity)


if kelayakan_air < 50:
    kelayakan_air = "Tidak Layak"
else:
    kelayakan_air = "Layak"
# Tampilkan Hasil
print(f"=== Hasil Fuzzy Logic ===")
print(f"Suhu (°C): {suhu}")
print(f"pH: {pH}")
print(f"TDS (ppm): {TDS}")
print(f"Turbidity: {turbidity} NTU")
print(f"Kelayakan Air: {kelayakan_air}")


# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/data', methods=['POST'])
# def receive_data():
#     try:
#         data = request.get_json()

#         if not data:
#             return jsonify({"status": "error", "message": "No JSON received"}), 400
        
#         # Cek apakah semua data sensor ada
#         required_keys = ["temperature", "ph", "tds", "turbidity", "kelayakan"]
#         for key in required_keys:
#             if key not in data:
#                 return jsonify({"status": "error", "message": f"Missing key: {key}"}), 400

#         print("Received Data:", data)
#         return jsonify({"status": "success", "message": "Data received"}), 200

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


# from pymongo import MongoClient
# from datetime import datetime
# import pytz  # Import untuk timezone Jakarta
# import random
# import time

# # Koneksi ke MongoDB
# client = MongoClient("mongodb+srv://indra:nnBigGhtZnZizObM@hostdb.vbod5.mongodb.net/?retryWrites=true&w=majority&appName=HostDB")
# db = client["water_quality"]
# collection = db["testing_sensor"]

# jakarta_tz = pytz.timezone("Asia/Jakarta")

# try:
#     # Looping hingga 100 kali
#     for _ in range(100):
#         # Ambil waktu saat ini dalam zona waktu Jakarta
#         timestamp = datetime.now(jakarta_tz).strftime('%Y-%m-%d %H:%M:%S')

#         # Simulasi data sensor dengan nilai acak
#         sensor_data = {
#             "timestamp": timestamp,
#             "ph": round(random.uniform(6.5, 8.5), 2),
#             "temperature": round(random.uniform(20, 30), 2),
#             "tds": round(random.uniform(100, 500), 2),
#             "turbidity": round(random.uniform(0, 5), 2),
#             "water_quality": random.choice(["Layak", "Tidak Layak"])
#         }

#         # Menyimpan data ke database
#         collection.insert_one(sensor_data)
#         print(f"Data disimpan: {sensor_data}")

#         # Tunggu 2 detik sebelum membaca data lagi
#         time.sleep(2)

# except KeyboardInterrupt:
#     print("\nProgram dihentikan oleh pengguna.")

# import secrets
# print(secrets.token_hex(32))  # Generates a 64-character (32-byte) secure key
# from pymongo import MongoClient

# MONGO_URI = "mongodb+srv://indra:nnBigGhtZnZizObM@hostdb.vbod5.mongodb.net/?retryWrites=true&w=majority&appName=HostDB"

# try:
#     client = MongoClient(MONGO_URI)
#     db = client["water_quality"]
#     print("✅ Connected to MongoDB:", db.name)
# except Exception as e:
#     print("❌ Connection failed:", e)
