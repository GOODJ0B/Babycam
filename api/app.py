#!/usr/bin/env python
import bme280
import smbus2
from flask import Flask, render_template, Response
from flask_cors import CORS
from importlib import import_module

# remove _pi to use test stream
from camera_pi import Camera

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'online'


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/values', methods=['GET'])
def values():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
