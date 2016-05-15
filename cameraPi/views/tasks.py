from flask import jsonify

from base import BaseView
from cameraPi import task_manager, pin_manager


class AllView(BaseView):
    def status(self):
        pin_results = pin_manager.get_info()
        task_results = task_manager.get_info()
        return jsonify(results=[pin_results, task_results])
