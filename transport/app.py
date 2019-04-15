"""
The main module for this flask application.
Sets up routes and provides AJAX and websocket methods.
"""
import csv
from dataclasses import dataclass
from importlib import resources
import logging.config
import os
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from transport.query import get_train_live
from transport.trie import Trie

log = logging.getLogger(__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('ftu_secret_key', 'secret')
bootstrap = Bootstrap(app)
socket_io = SocketIO(app)


@app.route('/')
def get_train_times():
    """
    Render the initial page
    """
    log.debug(f'request={request}')
    return render_template('train_times.html')


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    """
    Searches the trie for autocomplete suggestions.
    """
    log.debug(f'request={request}')
    query = request.args.get('q')
    suggestions = []
    for station in trie.search(query):
        suggestions.append(station.name)
    log.debug(f'autocomplete results={suggestions}')
    return jsonify(matching_results=suggestions)


@socket_io.on('connect', namespace='/train')
def train_connect():
    """
    Called when a websocket client connects.
    """
    log.debug('train_connect() called')


@socket_io.on('disconnect', namespace='/train')
def train_disconnect():
    """
    Called when a websocket client disconnects.
    """
    log.debug(f'train_disconnect() called')


@socket_io.on('search_event', namespace='/train')
def train_search(message):
    """
    Returns the live departure times for a particular station.
    """
    log.debug(f'received message: {message}')
    search_result = trie.search(message.get('station'))
    log.debug(f'search_result={search_result}')
    if search_result:
        trains = get_train_live(search_result[0].code)
        emit('train_result', trains, json=True)
        emit('station_name', {'station_name': message.get('station')})


@socket_io.on_error_default
def default_error_handler(e):
    """
    Called when a websocket error occurs.
    """
    log.exception(e)


@dataclass(frozen=True)
class Station:
    """
    Station name to CRS code mapping. Stored as a value in the trie.
    """
    name: str
    code: str


def create_trie() -> Trie:
    """
    Create a Trie data structure from the packaged csv file.
    :return: the trie
    """
    trie = Trie()
    with resources.open_text('transport', 'station_codes.csv') as stations:
        rows = csv.reader(stations)
        next(rows)  # skip the header
        for row in rows:
            station = Station(name=row[0], code=row[1])
            trie.insert(key=station.name, value=station)
    log.debug('trie built')
    return trie


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        level=os.getenv('ftu_log_level', 'DEBUG'))
    log.info('Starting transport UI')
    trie = create_trie()
    if os.getenv('ftu_fake_it', False):
        from transport.query import get_train_fake as get_train_live
    socket_io.run(app, host='0.0.0.0')
