from flask import send_file

from base import BaseView
from cameraPi import app


class CamView(BaseView):
    def status(self):
        frame = app.camera.get_frame()
        return send_file(frame, mimetype='image/jpg')
