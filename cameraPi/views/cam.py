from flask import Response

from base import BaseView
from cameraPi import app


class CamView(BaseView):
    def status(self):
        """ Get a single frame from the camera and return it
        """
        frame = app.camera.get_frame()
        return Response(frame, mimetype='image/jpg')
