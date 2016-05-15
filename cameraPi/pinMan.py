from subprocess import check_output, call


class PinManager(object):
    def __init__(self, pin_config):
        self.pin_config = pin_config

        # start out with all pins off
        for pin in self.pin_config:
            call(['gpio', 'export', str(pin), 'out'])
            call(['gpio', '-g', 'write', str(pin), '0'])

    def get_info(self, pin_id=None):
        if pin_id is None:
            result = {}
            for pin in self.pin_config:
                pin_status = int(check_output(['gpio', '-g', 'read', str(pin)]))
                result.update({pin: pin_status})
        else:
            pin_status = int(check_output(['gpio', '-g', 'read', str(pin_id)]))
            result = {pin_id: pin_status}

        return result

    def toggle(self, pin_id):
        pin_status = self.get_info(pin_id)

        if pin_status == 0:
            self.start(pin_id)
        else:
            self.stop(pin_id)

    def start(self, pin_id):
        call(['gpio', '-g', 'write', str(pin_id), '1'])
        # logger.info('Turned pin {pin} on'.format(pin=pin))

    def stop(self, pin_id):
        call(['gpio', '-g', 'write', str(pin_id), '0'])
        # logger.info('Turned pin {pin} off'.format(pin=pin))
