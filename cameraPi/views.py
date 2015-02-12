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
# pins = {}

for pin in pins:
   GPIO.setup(pin,GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)


@app.route("/get_status")
def get_status():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   pindata = dict(pins=pins)
   return jsonify(pindata)

@app.route("/toggle_pin/<toggle_pin>")
def toggle_pin(toggle_pin=None):
   try:
      for pin in pins:
         pins[pin]['state'] = GPIO.input(pin)

      toggle_pin = int(toggle_pin)

      if pins[toggle_pin]['state'] == 0:
         GPIO.output(toggle_pin, GPIO.HIGH)

      if pins[toggle_pin]['state'] == 1:
         GPIO.output(toggle_pin, GPIO.LOW)

      return jsonify(dict(result=True))
   except Exception as e:
      logger.exception(e)
      return jsonify(dict(result=False))

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
