from flask import jsonify

from base import BaseView
from cameraPi import task_manager


class CamView(BaseView):
    def status(self):
        cam_status = task_manager.get_info('cam')
        return jsonify(results=cam_status)

    def start(self):
        task_manager.start('cam')
        results = {
            'name': 'cam',
            'state': True,
            'success': True,
        }
        return jsonify(results=results)

    def stop(self):
        task_manager.stop('cam')
        results = {
            'name': 'cam',
            'state': False,
            'success': True,
        }
        return jsonify(results=results)
