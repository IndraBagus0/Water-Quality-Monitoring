import requests
import json
import time
import random

URL = "http://139.59.32.24:5000/data"

def generate_dummy_data():
    return {
        "temperature": round(random.uniform(20, 35), 1),  # Suhu antara 20-35 °C
        "ph": round(random.uniform(6, 8), 1),  # pH antara 6-8
        "tds": random.randint(100, 500),  # TDS antara 100-500 PPM
        "turbidity": round(random.uniform(10, 50), 1),  # Kekeruhan antara 10-50 NTU
        "kelayakan": random.choice(["layak", "tidak layak"])  # Status acak
    }

def send_data():
    while True:
        data = generate_dummy_data()
        response = requests.post(URL, json=data)
        
        if response.status_code == 200:
            print(f"✅ Data sent: {data}")
        else:
            print(f"❌ Failed to send data: {response.text}")

        time.sleep(5)  # Tunggu 5 detik sebelum mengirim lagi

if __name__ == "__main__":
    send_data()
