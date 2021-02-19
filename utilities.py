import flask
from flask_cors import CORS
import smbus2
import bme280
from os import listdir
from os.path import isfile, join

app = flask.Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return 'Online.'

@app.route('/screenshots', methods=['GET'])
def getScreenshots():
    files = [f for f in listdir('/home/pi/Babycam/AngularClient/dist/BabyCam/media') if isfile(join('/home/pi/Babycam/AngularClient/dist/BabyCam/media', f))]

    return files

@app.route('/values', methods=['GET'])
def sendCommand():
    print('=> getting values')
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)

    temperature = str(int(data.temperature))
    humidity = str(int(data.humidity))
    pressure = str(int(data.pressure))

    return "{\"temperature\":%s,\"humidity\":%s,\"pressure\":%s}" % (temperature, humidity, pressure)

app.run(host='0.0.0.0')