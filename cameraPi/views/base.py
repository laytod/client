from flask.ext.classy import FlaskView


class BaseView(FlaskView):
    @classmethod
    def get_view_info(cls):
        methods = ['status', 'toggle', 'start', 'stop']
        not_implemented = []
        for method in methods:
            try:
                getattr(cls(), method)()
            except NotImplementedError:
                not_implemented.append(method)
            except Exception:
                pass

        return list(set(methods) - set(not_implemented))

    def status(self):
        """
            [
                {
                    'name': str,
                    'data': dict
                }
            ]
        """
        raise NotImplementedError()

    def toggle(self):
        """
            {
                'name': str,
                'state': bool,
                'success': bool
            }
        """
        raise NotImplementedError()

    def start(self):
        """
            {
                'name': str,
                'state': bool,
                'success': bool
            }
        """
        raise NotImplementedError()

    def stop(self):
        """
            {
                'name': str,
                'state': bool,
                'success': bool
            }
        """
        raise NotImplementedError()
