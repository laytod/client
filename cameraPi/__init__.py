import logging
import xmlrpclib
import ConfigParser
from os import path
from hashlib import sha1
import supervisor.xmlrpc
from logging.handlers import RotatingFileHandler

from flask import Flask
app = Flask(__name__)

# parse the config
config = ConfigParser.ConfigParser()
config_path = path.dirname(path.dirname(path.realpath(__file__))) + '/camserv.conf'
config.read(config_path)

app.api_key = sha1(config.get('api', 'key')).hexdigest()

# Sessions variables are stored client side, on the users browser
# the content of the variables is encrypted, so users can't
# actually see it. They could edit it, but again, as the content
# wouldn't be signed with this hash key, it wouldn't be valid
# You need to set a scret key (random text) and keep it secret
app.secret_key = 'super secret key'

# Setup logging
# The logger will write to the same log file until it reaches
# maxBytes, and then will start a new log file and make a backup
# of the full log file.  A total of backupCount backup files
# will be made
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

#handler = RotatingFileHandler(config.get('logs', 'main'), maxBytes=10000)
#formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s',
#								datefmt='%Y-%m-%d %H:%M:%S')
#handler.setFormatter(formatter)
#logger.addHandler(handler)


# Setup xmlrpc control of supervisor
supervisor_xmlrpc = xmlrpclib.ServerProxy(
	'http://127.0.0.1',
	transport=supervisor.xmlrpc.SupervisorTransport(
		None,
		None,
		'unix:///run/supervisor.sock'
	)
)



import cameraPi.views
