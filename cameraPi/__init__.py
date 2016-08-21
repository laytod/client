
import logging
import ConfigParser
from os import path
# from hashlib import sha1
# from logging.handlers import RotatingFileHandler


from flask import Flask, Response, render_template
app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/var/log/camserv/camserv.log')
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
app.logger.addHandler(handler)


# parse the config
config = ConfigParser.ConfigParser()
config_path = path.dirname(path.dirname(path.realpath(__file__))) + '/camserv.conf'
config.read(config_path)


from pinMan import PinManager
from taskMan import TaskManager


pin_manager = PinManager(dict(config.items('pins')))
task_manager = TaskManager()
# app.api_key = sha1(config.get('api', 'key')).hexdigest()

# Sessions variables are stored client side, on the users browser
# the content of the variables is encrypted, so users can't
# actually see it. They could edit it, but again, as the content
# wouldn't be signed with this hash key, it wouldn't be valid
# You need to set a secret key (random text) and keep it secret
# app.secret_key = 'super secret key'

# Setup logging
# The logger will write to the same log file until it reaches
# maxBytes, and then will start a new log file and make a backup
# of the full log file.  A total of backupCount backup files
# will be made
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# handler = RotatingFileHandler(config.get('logs', 'main'), maxBytes=10000)
# formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s',
#                               datefmt='%Y-%m-%d %H:%M:%S')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


from cameraPi.views.cam import CamView
from cameraPi.views.pir import PirView
from cameraPi.views.pin import PinView
from cameraPi.views.tasks import AllView

CamView.register(app, route_base='/cam/')
PirView.register(app, route_base='/pir/')
PinView.register(app, route_base='/pin/')
AllView.register(app, route_base='/all/')

print '-----GPIO SERVER------'
routes = []
for rule in app.url_map.iter_rules():
    routes.append(rule.rule)

routes.sort()
for i in routes:
    print i
print '-------'


# @app.after_request
# def print_response(response):
#     print response.data
#     return response

# import time


def gen(camera):
    """Video streaming generator function."""
    path = '/run/shm/tmp.jpg'
    while True:
        time.sleep(2)
        # frame = camera.get_frame()
        try:
            with open(path, 'r') as stream_img:
                frame = stream_img.read()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception:
            pass

from camera import Camera
app.camera = Camera()


@app.route('/test_feed')
def index():
    return render_template('feed.html')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
