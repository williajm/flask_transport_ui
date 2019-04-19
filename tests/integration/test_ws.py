"""
Requires the application to be running.
"""
import json
import re
import pytest
import socketio


class CustomNamespace(socketio.ClientNamespace):

    connected = False
    train_result = []
    station_name = None

    @staticmethod
    def on_connect():
        CustomNamespace.connected = True

    @staticmethod
    def on_disconnect():
        CustomNamespace.connected = False

    @staticmethod
    def on_station_name(data):
        CustomNamespace.station_name = data.get('station_name')

    @staticmethod
    def on_train_result(data):
        CustomNamespace.train_result.append(data)

    @staticmethod
    def clear():
        CustomNamespace.train_result = []
        CustomNamespace.station_name = None


@pytest.fixture(scope='function')
def sio():
    sio = socketio.Client()
    sio.register_namespace(CustomNamespace('/train'))
    sio.connect('http://localhost:5000')
    sio.sleep(1)
    yield sio
    sio.disconnect()
    CustomNamespace.clear()


def test_connect(sio):
    assert CustomNamespace.connected


def test_disconnect(sio):
    sio.disconnect()
    assert not CustomNamespace.connected


def test_search(sio):
    sio.emit('search_event', {'station': 'Southampton Central'}, namespace='/train')
    sio.sleep(1)
    assert len(CustomNamespace.train_result) == 1
    result = json.loads(CustomNamespace.train_result[0])
    assert len(result) == 12
    for departure in result:
        assert len(departure.keys()) == 7
        assert re.match(pattern='^[0-2][0-9]:[0:5][0:9]$', string=departure.get('aimed_departure_time'))
        assert re.match(pattern='^[0-2][0-9]:[0:5][0:9]$', string=departure.get('expected_departure_time'))
        assert departure.get('destination_name').startswith('SOU destination')
        assert re.match(pattern='^[0-1]?[0-9]$', string=departure.get('platform'))
        assert departure.get('operator_name') == 'SOU operator'
        assert departure.get('origin_name').startswith('SOU origin')
        assert re.match(pattern='^(ON TIME|CANCELLED)$', string=departure.get('status'))
