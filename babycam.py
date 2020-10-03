# Babycam Python example
# Based on Source code from the official PiCamera package and RPi.bme280 examples

import smbus2
import bme280

import io
import picamera
import logging
import socketserver
import RPi.GPIO as GPIO

from threading import Condition
from http import server

#setup gpio for nightlight
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)


PAGE="""\
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<title>BabyCam</title>
</head>
<body style="background-color:black;">
<center><img src="stream.mjpg" width="640" height="480"></center>
<center><a href="#" onclick="$.get('liteon.html');">Light On</a>
        <a href="#" onclick="$.get('liteoff.html');">Light Off</a></center>
<div style="color:white;"><center> Room Temperature: <span id="temp">---</span> &#8451;</center>
<center> Room Humidity: <span id="humi">---</span> rH</center>
<center> Room Pressure: <span id="press">---</span> hPa</center>
</div><script>
var myVar = setInterval(myTimer, 10000);

function myTimer() {
  var d = new Date();
  $.get('roomtemp.html', function(data){document.getElementById("temp").innerHTML = data; });
  $.get('roompres.html', function(data){document.getElementById("press").innerHTML = data; });
  $.get('roomhumi.html', function(data){document.getElementById("humi").innerHTML = data; });
  
}
</script>
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        
        elif self.path == '/roomtemp.html':
            port = 1
            address = 0x76
            bus = smbus2.SMBus(port)
            calibration_params = bme280.load_calibration_params(bus, address)
            data = bme280.sample(bus, address, calibration_params)
            roomPress = data.pressure
            roomHumid = data.humidity
            
            # temp reads 10 degrees high for some reason...
            content = str(int(data.temperature-10)).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/roomhumi.html':
            port = 1
            address = 0x76
            bus = smbus2.SMBus(port)
            calibration_params = bme280.load_calibration_params(bus, address)
            data = bme280.sample(bus, address, calibration_params)       
            # temp reads 10 degrees high for some reason...
            content = str(int(data.humidity)).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)           
        elif self.path == '/roompres.html':
            port = 1
            address = 0x76
            bus = smbus2.SMBus(port)
            calibration_params = bme280.load_calibration_params(bus, address)
            data = bme280.sample(bus, address, calibration_params)
            
            # temp reads 10 degrees high for some reason...
            content = str(int(data.pressure)).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
            
        elif self.path == '/liteon.html':
            GPIO.output(27,GPIO.HIGH)
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/liteoff.html':
            GPIO.output(27,GPIO.LOW)
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()