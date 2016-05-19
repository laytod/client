from flask import jsonify
from flask.ext.classy import route
from devServer import app


def fake_status(self):
    result = [
        {
            'name': 'fake name',
            'data': dict()
        }
    ]
    return jsonify(result=result)


def fake_all_status(self):
    result = [
        {
            'type': 'cam',
            'state': app.cam_state,
            'data': dict()
        },
        {
            'type': 'pir',
            'state': app.pir_state,
            'data': dict()
        },
    ]

    for pin, name in app.pin_config.iteritems():
        result.append({
            'type': 'pin',
            'state': app.pin_state[pin],
            'data': {
                'pin_id': pin,
                'name': name,
            }
        })

    return jsonify(results=result)


@route('/toggle/')
def fake_toggle(self):
    base = self.get_route_base()
    base_string = base + '_state'
    state = getattr(app, base_string)
    setattr(app, base_string, not state)

    result = {
        'name': base,
        'state': getattr(app, base_string),
        'success': True
    }
    return jsonify(result=result)


@route('/toggle/<pin_id>')
def fake_toggle_pin(self, pin_id):
    app.pin_state[pin_id] = not app.pin_state[pin_id]
    result = {
        'name': 'fake name',
        'state': app.pin_state[pin_id],
        'success': True
    }
    return jsonify(result=result)


def fake_start(self):
    result = {
        'name': 'fake name',
        'state': True,
        'success': True
    }
    return jsonify(result=result)


def fake_stop(self):
    result = {
        'name': 'fake name',
        'state': True,
        'success': True
    }
    return jsonify(result=result)
