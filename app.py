from flask import Flask, render_template
from src import *


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/monitoring')
def monitoring():
    monitoring_data = get_data()

    return render_template('monitoring.html', data=monitoring_data)

@app.errorhandler(403)
def forbidden(error):
    return render_template('error-403.html'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error-404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error-500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)