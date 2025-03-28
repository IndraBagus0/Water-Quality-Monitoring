from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, Response
from markupsafe import Markup
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import json
import time
import random
import threading
from src import *
from bson import ObjectId, Binary
from configs import Config
import base64
from datetime import datetime
import pytz 

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
mongo = PyMongo(app)
latest_data = {}
jakarta_tz = pytz.timezone("Asia/Jakarta")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Sesi login anda telah habis', 'warning')
        return redirect(url_for('login'))
    user = database_users.find_one({"_id": ObjectId(session["user_id"])})
    list_admin = admin_data()
    return render_template('dashboard.html', user=user, list_admin=list_admin)

@app.route('/monitoring')
def monitoring():
    if 'user_id' not in session:
        flash('Sesi login anda telah habis', 'warning')
        return redirect(url_for('login'))
    monitoring_data = get_data()
    return render_template('monitoring.html', data=monitoring_data)

@app.route('/device-list', methods=['GET'])
def device_list():
    try:
        devices = list(database_alat.find({}, {"_id": 0, "device_id": 1}))
        device_count = len(devices)  # Hitung jumlah perangkat
        
        return jsonify({"status": "success", "devices": devices, "count": device_count}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/list-users')
def users():
    list_user = admin_data()
    print(list_user)
    return render_template('users.html', list_user=list_user)

@app.route('/filter-monitoring', methods=['GET'])
def filter_monitoring():
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    if not start_date or not end_date:
        return jsonify({"error": "Tanggal tidak valid"}), 400

    try:
        start_dt = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")

        filtered_data = database_sensor.find({
            "timestamp": {"$gte": start_date, "$lte": end_date}
        }).sort('timestamp', -1)

        result = []
        for idx, record in enumerate(filtered_data, start=1):
            result.append({
                "no": idx,
                "timestamp": record['timestamp'], 
                "ph": record['ph'],
                "temperature": f"{record['temperature']} Derajat",
                "tds": f"{record['tds']} PPM",
                "turbidity": f"{record['turbidity']} NTU",
                "kelayakan": record['kelayakan']
            })

        return jsonify(result)

    except ValueError:
        return jsonify({"error": "Format tanggal salah"}), 400

@app.route('/data', methods=['POST'])
def receive_data():
    global latest_data
    try:
        api_key = request.headers.get("X-API-KEY")
        if not api_key:
            return jsonify({"status": "error", "message": "API Key is missing"}), 401

        device = database_alat.find_one({"api_key": api_key})
        if not device:
            return jsonify({"status": "error", "message": "Invalid API Key"}), 403
        location = device.get("location", "Unknown")
        print(location)
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON received"}), 400

        required_keys = ["temperature", "ph", "tds", "turbidity", "kelayakan"]
        for key in required_keys:
            if key not in data:
                return jsonify({"status": "error", "message": f"Missing key: {key}"}), 400
        timestamp = datetime.now(jakarta_tz).strftime('%Y-%m-%d %H:%M:%S')
        sensor_entry = {
            "device_id": device["_id"], 
            "location": location, 
            "temperature": data["temperature"],
            "ph": data["ph"],
            "tds": data["tds"],
            "turbidity": data["turbidity"],
            "kelayakan": data["kelayakan"],
            "timestamp": timestamp
        }
        database_sensor.insert_one(sensor_entry)
        print("Data received:", sensor_entry)
        latest_data = sensor_entry  

        return jsonify({"status": "success", "message": "Data received"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/stream')
def stream():
    print("Client connected to SSE")
    def event_stream():
        global latest_data
        while True:
            if latest_data:
                data_copy = latest_data.copy()
                data_copy.pop("_id", None)
                data_copy["device_id"] = str(data_copy["device_id"]) if isinstance(data_copy["device_id"], ObjectId) else data_copy["device_id"]
                yield f"data: {json.dumps(data_copy)}\n\n"
            time.sleep(2)

    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/add-device', methods=['POST'])
def add_device():
    try:
        data = request.get_json()
        device_id = data.get("device_id")
        location = data.get("location")

        if not device_id or not location:
            return jsonify({"status": "error", "message": "Device ID dan Lokasi harus diisi"}), 400

        api_key = save_api_key(device_id, location)
        return jsonify({"status": "success", "api_key": api_key}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8') if data else ''

@app.route('/profile', methods=["GET", "POST"]) 
def profile():
    if 'user_id' not in session:
        flash('Sesi login anda telah habis', 'warning')
        return redirect(url_for('login'))
    
    user = database_users.find_one({"_id": ObjectId(session["user_id"])})

    if request.method == 'POST':
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")

        # Jika user ingin mengganti password
        if old_password and new_password:
            if not user or "password" not in user:
                flash("Terjadi kesalahan, silakan login ulang.", "danger")
                return redirect(url_for('profile'))

            # Verifikasi password lama
            if not check_password_hash(user["password"], old_password):
                flash("Kata sandi lama salah!", "danger")
                return redirect(url_for('profile'))

            # Hash password baru dan update di database
            hashed_new_password = generate_password_hash(new_password)
            database_users.update_one(
                {"_id": ObjectId(session["user_id"])},
                {"$set": {"password": hashed_new_password}}
            )

            flash("Berhasil mengubah kata sandi!", "success")
            return redirect(url_for('profile'))

        # Update data lain (tanpa mengubah password)
        updated_data = {
            "name": request.form.get("name", "").strip() or "Belum di isi",
            "username": request.form.get("username", "").strip() or "Belum di isi",
            "email": request.form.get("email", "").strip() or "Belum di isi",
            "phone": request.form.get("phone", "").strip() or "Belum di isi",
            "address": request.form.get("address", "").strip() or "Belum di isi"
        }

        # Jika ada upload foto profil
        if "profile_pic" in request.files:
            file = request.files["profile_pic"]
            if file.filename != "":
                image_data = file.read()
                updated_data["profile_pic"] = Binary(image_data)

        database_users.update_one(
            {"_id": ObjectId(session["user_id"])}, 
            {"$set": updated_data}
        )

        flash("Profil berhasil diperbarui!", "success")
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

@app.errorhandler(403)
def forbidden(error):
    return render_template('error-403.html'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error-404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error-500.html'), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if database_users.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        elif database_users.find_one({'email': email}):
            flash('Email already exists. Please use a different email.', 'danger')
        else:
            hashed_password = generate_password_hash(password) 
            database_users.insert_one({'username': username, 'email': email, 'password': hashed_password})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login')) 

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = database_users.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id']) 
            session['email'] = user['email']
            session['username'] = user['username']
            # flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))  
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Kamu telah logout.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)