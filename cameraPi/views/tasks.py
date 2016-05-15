from flask import jsonify

from base import BaseView
from cameraPi import task_manager


class AllView(BaseView):
    def status(self):
        results = task_manager.get_info()
        return jsonify(results=results)
