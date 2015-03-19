import datetime
from subprocess import check_output, call

from flask import jsonify, request, Response
from cameraPi import app, logger, supervisor_xmlrpc
#from cameraPi.email import send_email

pins = { 17 : {'name': 'green'},
         22 : {'name': 'red'},
         23 : {'name': 'night vision'}
}

def get_pin_status(pin):
    return int(check_output(['gpio', '-g', 'read', str(pin)]))

def toggle_gpio(pin):
    pin_status = get_pin_status(pin)

    if pin_status == 0:
        call(['gpio', '-g', 'write', str(pin), '1'])
        logger.info('Turned pin {pin} on'.format(pin=pin))
    else:
        call(['gpio', '-g', 'write', str(pin), '0'])
        logger.info('Turned pin {pin} off'.format(pin=pin))

# start out with all pins off
for pin in pins:
    call(['gpio', 'export', str(pin), 'out'])
    call(['gpio', '-g', 'write', str(pin), '0'])


def get_status(pins):
    status = dict(pins)
    for pin in pins:
        pin_status = get_pin_status(pin)
        status[pin].update(state=pin_status) 

    return status


@app.route("/pin_status")
def pin_status():
   status = get_status(pins)
   return jsonify(status)


@app.route("/toggle_pin/<pin>")
def toggle_pin(pin=None):
    try:
        pin = int(pin)
        toggle_gpio(pin)
        return jsonify(get_status(pins))
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


#@app.route('/email')
#def email():
#  admins = ['laytod@gmail.com']
#  send_email(recipients=admins, subject='fake subject', body='fake body for a fake email')
#  logger.info('Sent email to {admins}'.format(admins=admins))
#  return 'email sent'

#def gen(camera):
#    while True:
#        frame = camera.get_frame()
#        yield (b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
#@app.route('/video_feed')
#def video_feed():
#    return Response(gen(Camera()),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')
