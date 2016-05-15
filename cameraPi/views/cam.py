from base import BaseView


class CamView(BaseView):
    def status(self):
        return 'cam status'

    def toggle(self):
        return 'cam toggle'
