import datetime
import RPi.GPIO as GPIO

from flask import jsonify, request
from cameraPi import app, logger, supervisor_xmlrpc

GPIO.setmode(GPIO.BCM)
## GPIO.cleanup()
GPIO.setwarnings(False)

pins = { 17 : {'name': 'green'},
         22 : {'name': 'red'},
         23 : {'name': 'night vision'}
}

# start out with all pins off
for pin in pins:
   GPIO.setup(pin,GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)


def get_status(pins):
   status = dict(pins)
   for pin in pins:
      status[pin].update(state=GPIO.input(pin))

   return status


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

      return jsonify(status)
   except Exception as e:
      logger.exception(e)
      raise


def get_supervisor_process_info(name='all'):
   if name == 'all':
      process_info = supervisor_xmlrpc.supervisor.getAllProcessInfo()
   else:
      process_info = supervisor_xmlrpc.supervisor.getProcessInfo(name)

   return process_info


@app.route('/process_info', defaults={'name': 'all'})
@app.route('/process_info/<name>')
def process_info(name='all'):
   return jsonify(get_supervisor_process_info(name))


def start_supervisor_process(name):
   return supervisor_xmlrpc.supervisor.startProcess(name)

def stop_supervisor_process(name):
   return supervisor_xmlrpc.supervisor.stopProcess(name)


@app.route('/toggle_video')
def toggle_video():
   processes = ['cam', 'mjpg']
   for process in processes:
      process_info = get_supervisor_process_info(process)

      if process_info['state'] != 0:
         result = stop_supervisor_process(process)
      else:
         result = start_supervisor_process(process)

   return jsonify({
      'result': result,
      'info': get_supervisor_process_info(process)
   })
