import datetime
import RPi.GPIO as GPIO

from flask import jsonify, request, redirect
from cameraPi import app, logger

GPIO.setmode(GPIO.BCM)
## GPIO.cleanup()
GPIO.setwarnings(False)

pins = { 17 : {'name': 'green', 'state': GPIO.LOW},
         22 : {'name': 'yellow', 'state': GPIO.LOW},
         23 : {'name': 'red', 'state': GPIO.LOW} }

for pin in pins:
   GPIO.setup(pin,GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/pin_status")
def pin_status():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   data = dict(pins=pins)
   return jsonify(data)


@app.route("/toggle_pin/<pin>")
def toggle_pin(pin=None):
   try:
      pin = int(pin)
      pin_status = GPIO.input(pin)

      if pin_status == 0:
         GPIO.output(pin, GPIO.HIGH)
         logger.info('Turned pin {pin} on'.format(pin=pin))
      elif pin_status == 1:
         GPIO.output(pin, GPIO.LOW)
         logger.info('Turned pin {pin} off'.format(pin=pin))

      return jsonify(dict(result=True))
   except Exception as e:
      logger.exception(e)
      return jsonify(dict(result=False))


def toggle_stream():
   pass
