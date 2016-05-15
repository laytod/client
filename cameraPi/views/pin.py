from flask import jsonify
from flask.ext.classy import route

from base import BaseView
from cameraPi import pin_manager


class PinView(BaseView):
    @route('/status/<pin_id>')
    def status(self, pin_id):
        results = pin_manager.get_info()
        return jsonify(results=results)

    @route('/toggle/<pin_id>')
    def toggle(self, pin_id):
        state = pin_manager.toggle(pin_id)
        results = {
            'name': pin_manager.pin_config[pin_id],
            'state': state,
            'success': True
        }
        return jsonify(results=results)

    @route('/start/<pin_id>')
    def start(self, pin_id):
        pin_manager.start(pin_id)
        results = {
            'name': pin_manager.pin_config[pin_id],
            'state': True,
            'success': True,
        }
        return jsonify(results=results)

    @route('/stop/<pin_id>')
    def stop(self, pin_id):
        pin_manager.stop(pin_id)
        results = {
            'name': pin_manager.pin_config[pin_id],
            'state': False,
            'success': True,
        }
        return jsonify(results=results)
