from flask import jsonify

from base import BaseView
from cameraPi import task_manager


class PirView(BaseView):
    def status(self):
        pir_status = task_manager.get_info('pir')
        results = {
            'name': 'pir',
            'state': pir_status['statename'] == 'RUNNING',
            'data': {}
        }
        return jsonify(results=results)

    def start(self):
        task_manager.start('pir')
        results = {
            'name': 'pir',
            'state': True,
            'success': True,
        }
        return jsonify(results=results)

    def stop(self):
        task_manager.stop('pir')
        results = {
            'name': 'pir',
            'state': False,
            'success': True,
        }
        return jsonify(results=results)
