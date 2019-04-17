"""
Requires the application to be running.
"""
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
