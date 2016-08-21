from flask import Response

from base import BaseView
from cameraPi import app


class CamView(BaseView):
    def status(self):
        frame = app.camera.get_frame()
        return Response(frame, mimetype='image/jpg')
