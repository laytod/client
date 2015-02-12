import datetime
import RPi.GPIO as GPIO

from flask import jsonify, request, redirect
from cameraPi import app, logger

# give alias to logger
# logger = app.logger


GPIO.setmode(GPIO.BCM)
## GPIO.cleanup()
GPIO.setwarnings(False)

pins = { 17 : {'name': 'green', 'state': GPIO.LOW},
         22 : {'name': 'yellow', 'state': GPIO.LOW},
         23 : {'name': 'red', 'state': GPIO.LOW} }
# pins = {}

for pin in pins:
   GPIO.setup(pin,GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)


@app.route("/get_pin_status")
def index():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   pindata = dict(pins=pins)
   return jsonify(pindata)


# The function below is executed when someone requests a URL with the pin number and action in it:
# @app.route("/changePin")
# def action():
#    action = request.args.get('action', None)
#    pin = request.args.get('pin', None)
#    pin = int(pin)

#    try:
#       if action == 'off':
#          GPIO.output(pin, GPIO.HIGH)
#       elif action == 'on':
#          GPIO.output(pin, GPIO.LOW)

#       result = True
#    except:
#       result = False

#    logger.info('Turned pin {pin} {action}'.format(
#          pin=pin,
#          action=action))
#    return jsonify(result=result)
