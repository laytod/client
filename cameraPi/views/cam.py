from flask import jsonify

from base import BaseView
from cameraPi import task_manager


class CamView(BaseView):
    def status(self):
        task_status = task_manager.get_info()
        cam_state = False
        mjpg_state = False

        for task in task_status:
            name = task['name']
            if name == 'cam':
                cam_state = task['statename'] == 'RUNNING'
            elif name == 'mjpg':
                mjpg_state = task['statename'] == 'RUNNING'

        results = {
            'name': 'cam',
            'state': cam_state and mjpg_state,
            'data': {}
        }
        return jsonify(results=results)

    def start(self):
        task_manager.start('cam')
        task_manager.start('mjpg')
        results = {
            'name': 'cam',
            'state': True,
            'success': True,
        }
        return jsonify(results=results)

    def stop(self):
        task_manager.stop('cam')
        task_manager.stop('mjpg')
        results = {
            'name': 'cam',
            'state': False,
            'success': True,
        }
        return jsonify(results=results)
