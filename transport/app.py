import os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from transport.query import get_train_live
import logging
import logging.config

log = logging.getLogger(__name__)
app = Flask(__name__)
# TODO add secret
app.config['SECRET_KEY'] = 'secret!'
bootstrap = Bootstrap(app)
socket_io = SocketIO(app)


@app.route('/')
def get_train_times():
    log.info(f'request={request}')
    return render_template('train_times.html')


@socket_io.on('connect', namespace='/train')
def train_connect():
    log.info('train_connect() called')


@socket_io.on('disconnect', namespace='/train')
def train_disconnect():
    log.info(f'train_disconnect() called')


@socket_io.on('search_event', namespace='/train')
def train_search(message):
    log.info('received message: ' + str(message))
    trains = get_train_live(message.get('station'))
    emit('train_result', trains, json=True)


@socket_io.on_error_default
def default_error_handler(e):
    log.exception(e)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        level=os.getenv('ftu_log_level', 'DEBUG'))
    socket_io.run(app)
