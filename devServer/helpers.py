from flask.ext.classy import FlaskView
from fakeviews import fake_start, fake_stop, fake_toggle, fake_status, fake_all_status, fake_toggle_pin


def create_fake_view_classes(app):
    function_map = {
        'start': fake_start,
        'stop': fake_stop,
        'toggle': fake_toggle,
        'status': fake_status,
    }

    for method in ['cam', 'pir']:
        x = type(method, (FlaskView,), function_map)
        x.register(app, route_base='/' + method + '/')

    x = type('all', (FlaskView,), {'status': fake_all_status})
    y = type('pin', (FlaskView,), {'toggle': fake_toggle_pin})
    x.register(app, route_base='/' + 'all' + '/')
    y.register(app, route_base='/' + 'pin' + '/')


def get_all_routes(app):
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(rule.rule)

    routes.sort()
    return routes
