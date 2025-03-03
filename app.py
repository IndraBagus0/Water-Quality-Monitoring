from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import json
import time
import random
import threading
from src import *
from configs import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
mongo = PyMongo(app)
latest_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    print(session)
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/monitoring')
# @login_required
def monitoring():
    monitoring_data = get_data()
    if 'user_id' not in session:
        flash('Please log in to access the monitoring page.', 'warning')
        return redirect(url_for('login'))
    return render_template('monitoring.html', data=monitoring_data)

@app.route('/data', methods=['POST'])
def receive_data():
    global latest_data
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON received"}), 400

        required_keys = ["temperature", "ph", "tds", "turbidity", "kelayakan"]
        for key in required_keys:
            if key not in data:
                return jsonify({"status": "error", "message": f"Missing key: {key}"}), 400

        latest_data = data  # Simpan data terbaru
        print("Received Data:", data)

        return jsonify({"status": "success", "message": "Data received"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/stream')
def stream():
    print("Client connected to SSE")  # Tambahkan log untuk debug
    def event_stream():
        global latest_data
        while True:
            if latest_data:
                yield f"data: {json.dumps(latest_data)}\n\n"
            time.sleep(2)  # Update setiap 2 detik

    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to access the profile page.', 'warning')
        return redirect(url_for('login'))
    return render_template('profile.html')

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
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))  
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)