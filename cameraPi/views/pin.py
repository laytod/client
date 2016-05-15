from base import BaseView
from flask.ext.classy import route


class PinView(BaseView):
    @route('/status/<pin_id>')
    def status(self, pin_id):
        return 'pin {} status'.format(pin_id)

    @route('/toggle/<pin_id>')
    def toggle(self, pin_id):
        return 'toggle pin {}'.format(pin_id)

    @route('/start/<pin_id>')
    def start(self, pin_id):
        return 'start pin {}'.format(pin_id)

    @route('/stop/<pin_id>')
    def stop(self, pin_id):
        return 'stop pin {}'.format(pin_id)
