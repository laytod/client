import json

from subprocess import check_output, call

from flask import jsonify
from cameraPi import app, supervisor_xmlrpc
from decorators import require_api_key

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/var/log/camserv/camserv.log')
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

pins = {
    17: {'name': 'green'},
    22: {'name': 'red'},
    23: {'name': 'night vision'}
}


# def require_api_key(fn):
#     @wraps(fn)
#     def decorated(*args, **kwargs):
#         if request.headers.get('api-key') == app.api_key:
#             return fn(*args, **kwargs)
#         else:
#             abort(401)
#     return decorated


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
@require_api_key
def pin_status():
    logger.info('getting status')
    status = get_status(pins)
    return jsonify(status)


@app.route("/toggle_pin/<pin>")
@require_api_key
def toggle_pin(pin=None):
    try:
        pin = int(pin)
        toggle_gpio(pin)
        return jsonify(get_status(pins))
    except Exception as e:
        logger.exception(e)
        raise


@app.route('/toggle_video')
@require_api_key
def toggle_video():
    processes = ['cam', 'mjpg']
    for process in processes:
        process_info = get_supervisor_process_info(process)

        if process_info['state'] != 0:
            logger.info('Stopping {process}'.format(process=process))
            result = stop_supervisor_process(process)
        else:
            logger.info('Starting {process}'.format(process=process))
            result = start_supervisor_process(process)

    return jsonify({
        'result': result,
        'info': get_supervisor_process_info(process)
    })


@app.route('/start_motion_detection')
@require_api_key
def start_motion_detection():
    logger.info('Starting motion detection')
    process = 'pir'
    result = start_supervisor_process(process)
    return jsonify({
        'result': result,
        'info': get_supervisor_process_info(process)
    })


@app.route('/process_info', defaults={'name': 'all'})
@app.route('/process_info/<name>')
@require_api_key
def process_info(name='all'):
    process_list = get_supervisor_process_info(name)
    return json.dumps(process_list)


def get_supervisor_process_info(name='all'):
    if name == 'all':
        process_info = supervisor_xmlrpc.supervisor.getAllProcessInfo()
    else:
        process_info = supervisor_xmlrpc.supervisor.getProcessInfo(name)

    return process_info


def start_supervisor_process(name):
    return supervisor_xmlrpc.supervisor.startProcess(name)


def stop_supervisor_process(name):
    return supervisor_xmlrpc.supervisor.stopProcess(name)


# def gen(camera):
#    while True:
#        frame = camera.get_frame()
#        yield (b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
# @app.route('/video_feed')
# def video_feed():
#    return Response(gen(Camera()),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')
