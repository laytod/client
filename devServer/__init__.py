from flask import Flask
app = Flask(__name__)

# import real views
import sys
from os import path
real_view_path = path.dirname(path.dirname(path.abspath(__file__))) + '/cameraPi/views/'
sys.path.append(real_view_path)


from helpers import create_fake_view_classes, get_all_routes

import ConfigParser
# parse the config
config = ConfigParser.ConfigParser()
config_path = path.dirname(path.dirname(path.realpath(__file__))) + '/camserv.conf'
config.read(config_path)

# app.pin_config contains the pin id and the name of the pin
app.pin_config = dict(config.items('pins'))
pin_state = {}
for pin_id in app.pin_config:
    pin_state.update({pin_id: False})

app.pin_state = pin_state
app.cam_state = False
app.pir_state = False

create_fake_view_classes(app)


routes = get_all_routes(app)
print '-----------'
for i in routes:
    print i
print '-----------'
