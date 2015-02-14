import datetime
import RPi.GPIO as GPIO

from flask import jsonify, request, redirect
from cameraPi import app, logger

GPIO.setmode(GPIO.BCM)
## GPIO.cleanup()
GPIO.setwarnings(False)

pins = { 17 : {'name': 'green'},
         22 : {'name': 'yellow'},
         23 : {'name': 'red'}
}

for pin in pins:
   GPIO.setup(pin,GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/pin_status")
def pin_status():
   status = get_status(pins)
   return jsonify(status)


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

      status = get_status(pins)

      return jsonify(status))
   except Exception as e:
      logger.exception(e)


def get_status(pins):
   status = dict(pins)
   for pin in pins:
      status[pin].update(state=GPIO.input(pin))

   return status


def toggle_stream():
   pass
