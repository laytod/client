from flask import jsonify

from base import BaseView
from cameraPi import task_manager, pin_manager


class AllView(BaseView):
    def status(self):
        pin_results = pin_manager.get_info()
        task_results = task_manager.get_info()

        results = []
        for pin, pin_status in pin_results.iteritems():
            pin_name = pin_manager.pin_config[pin]
            results.append({
                'type': 'pin',
                'state': bool(pin_status),
                'data': {
                    'pin_id': pin,
                    'name': pin_name,
                }
            })

        cam_state = False
        mjpg_state = False
        pir_state = False

        for task in task_results:
            name = task['name']
            if name == 'cam':
                cam_state = task['statename'] == 'RUNNING'
            elif name == 'mjpg':
                mjpg_state = task['statename'] == 'RUNNING'
            elif name == 'pir':
                pir_state = task['statename'] == 'RUNNING'

        results.append({
            'type': 'cam',
            'state': cam_state and mjpg_state,
            'data': {}
        })

        results.append({
            'type': 'pir',
            'state': pir_state,
            'data': {}
        })

        return jsonify(results=results)
