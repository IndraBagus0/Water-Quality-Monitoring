from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

from src import *
from configs import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
# Initialize extensions
mongo = PyMongo(app)

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
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    return render_template('monitoring.html', data=monitoring_data)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
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

        # Cek apakah username atau email sudah ada di database
        if database_users.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        elif database_users.find_one({'email': email}):
            flash('Email already exists. Please use a different email.', 'danger')
        else:
            hashed_password = generate_password_hash(password)  # Hash password sebelum disimpan
            database_users.insert_one({'username': username, 'email': email, 'password': hashed_password})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))  # Pastikan ada route `/login`

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = database_users.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):  # Cek password hash
            session['user_id'] = str(user['_id'])  # Simpan ID user ke sesi
            session['email'] = user['email']
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))  # Arahkan ke dashboard
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Hapus semua sesi
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)