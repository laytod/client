from subprocess import check_output, call


class PinManager(object):
    def __init__(self, pin_config):
        self.pin_config = pin_config

        # start out with all pins off
        for pin in self.pin_config:
            self._export_pin(pin, 'out')
            self._write_to_pin(pin, 0)

    def get_info(self, pin_id=None):
        if pin_id is None:
            result = {}
            for pin in self.pin_config:
                pin_status = self._check_pin(pin)
                result.update({pin: pin_status})
        else:
            pin_status = self._check_pin(pin_id)
            result = {pin_id: pin_status}

        return result

    def toggle(self, pin_id):
        pin_status = self.get_info(pin_id)

        if pin_status == 0:
            self.start(pin_id)
        else:
            self.stop(pin_id)

        return not bool(pin_status)

    def start(self, pin_id):
        self._write_to_pin(pin_id, 1)
        # logger.info('Turned pin {pin} on'.format(pin=pin))

    def stop(self, pin_id):
        self._write_to_pin(pin_id, 0)
        # logger.info('Turned pin {pin} off'.format(pin=pin))

    def _write_to_pin(self, pin_id, value):
        cmd = 'gpio -g write {pin_id} {value}'.format(
            pin_id=pin_id,
            value=value,
        )
        call(cmd.split())

    def _check_pin(self, pin_id):
        cmd = 'gpio -g read {pin_id}'.format(
            pin_id=pin_id
        )
        return check_output(cmd.split())

    def _export_pin(self, pin_id, mode):
        cmd = 'gpio export {pin_id} {mode}'.format(
            pin_id=pin_id,
            mode=mode,
        )
        call(cmd.split())
