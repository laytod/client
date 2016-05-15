from base import BaseView


class PirView(BaseView):
    def status(self):
        return 'pir status'

    def start(self):
        return 'pir start'

    def stop(self):
        return 'pir_stop'
