from flask import Flask, render_template, redirect, url_for, request
from HeartRate import HeartRate
from flask_socketio import SocketIO, send, emit
from HeartRate import thread
import logging


logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s][%(levelname)s] - %(funcName)s: %(message)s')
logger = logging.getLogger(__name__)
# handler = logging.FileHandler(__builtin__.config['dir']['log_file_handler'])
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('[%(asctime)s][%(levelname)s] - %(funcName)s: %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)x

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
socketio.init_app(app, logger = True)

users = {'Kushan': 'Gupta', 'Brett': 'Medina'}


@socketio.on('message')
def handle_message(message):
    logging.info('received message: ' + message)


@app.route('/')
def index():
    logging.info("index page")
    return render_template('index.html')


@app.route('/welcome')
def welcome():
    logging.info("welcome page")
    return render_template("welcome.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        if request.form['username'] not in users or request.form['password'] != \
            users.get(username):
            error = 'Invalid credentials. Please try again.'
        else:
            return redirect(url_for('heartratepage'))
    return render_template('login.html', error=error)


@app.route('/heartratepage', methods=['GET'])
def heartratepage():
    hr = HeartRate()
    hrValue = hr.getHR()
    logging.info(hrValue)
    handle_message(hrValue)
    return hrValue


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    logging.info('Client Connected')
    heartRate = HeartRate()

    if not thread.isAlive():
        logging.info("Starting Thread")
        thread = heartRate.run(socketio)
        thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    logging.info('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
