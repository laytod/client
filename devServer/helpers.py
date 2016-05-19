from flask.ext.classy import FlaskView
from fakeviews import fake_start, fake_stop, fake_toggle, fake_status, fake_all_status, fake_toggle_pin


def create_fake_view_classes(app):
    function_map = {
        'start': fake_start,
        'stop': fake_stop,
        'toggle': fake_toggle,
        'status': fake_status,
    }

    for method in function_map.keys():
        x = type(method, (FlaskView,), function_map)
        x.register(app, route_base='/' + method + '/')


def get_all_routes(app):
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(rule.rule)

    routes.sort()
    return routes
