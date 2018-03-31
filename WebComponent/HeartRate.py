from firebase import firebase
from time import sleep
from threading import Thread, Event
import logging

logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s][%(levelname)s] - %(funcName)s: %(message)s')
logger = logging.getLogger(__name__)

thread = Thread()

class HeartRate(Thread):
    myDatabase = firebase.FirebaseApplication('https://bluefitnesshr.firebaseio.com', None)


    def __init__(self):
        self.thread_stop_event = Event()
        self.delay = 1
        self.heartRate = self.myDatabase.get('/heartrate', None)
        super(HeartRate, self).__init__()

    def getHR(self, SocketIO):
        while not self.thread_stop_event.isSet():
            logging.info(self.myDatabase.get('/heartrate', None))
            SocketIO.emit('heartRate', {'heartRate': self.myDatabase.get('/heartrate', None)}, namespace='/test')
            sleep(self.delay)

    def run(self, SocketIO):
        self.getHR(SocketIO)
