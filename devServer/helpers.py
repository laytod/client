from flask.ext.classy import FlaskView
from fakeviews import fake_start, fake_stop, fake_toggle, fake_status, fake_all_status, fake_toggle_pin


def get_function_map(methods):
    function_map = {}
    for method in methods:
        if method == 'start':
            fake_method = fake_start
        if method == 'stop':
            fake_method = fake_stop
        if method == 'toggle':
            fake_method = fake_toggle
        if method == 'status':
            fake_method = fake_status

        function_map.update({method: fake_method})
    return function_map


def create_fake_view_classes(app, view_methods):
    for method, methods in view_methods.iteritems():
        if method == 'all':
            # use a special fake_status for 'all' endpoint
            function_map = {'status': fake_all_status}
        elif method == 'pin':
            function_map = {'toggle': fake_toggle_pin}
        else:
            function_map = get_function_map(methods)
        x = type(method, (FlaskView,), function_map)
        x.register(app, route_base='/' + method + '/')


def get_all_routes(app):
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(rule.rule)

    routes.sort()
    return routes
