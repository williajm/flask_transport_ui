import csv
import os
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from transport.query import get_train_live
import logging
import logging.config
from importlib import resources
from transport.trie import Trie

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


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    log.info(f'request={request}')
    query = request.args.get('q')
    suggestions = []
    for suggestion in trie.search(query):
        suggestions.append(suggestion[0]) # TODO be more defensive
    log.info(f'autocomplete results={suggestions}')
    return jsonify(matching_results=suggestions)


@socket_io.on('connect', namespace='/train')
def train_connect():
    log.info('train_connect() called')


@socket_io.on('disconnect', namespace='/train')
def train_disconnect():
    log.info(f'train_disconnect() called')


@socket_io.on('search_event', namespace='/train')
def train_search(message):
    log.info('received message: ' + str(message))
    search_result = trie.search(message.get('station'))  # TODO sanitise
    log.info(f'search_result={search_result}')
    trains = get_train_live(search_result[0][1])
    emit('train_result', trains, json=True)


@socket_io.on_error_default
def default_error_handler(e):
    log.exception(e)


def create_trie() -> Trie:
    trie = Trie()
    with resources.open_text('transport', 'station_codes.csv') as stations:
        rows = csv.reader(stations)
        next(rows)
        for row in rows:
            trie.insert(row[0], row)
    return trie


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        level=os.getenv('ftu_log_level', 'DEBUG'))
    trie = create_trie()
    socket_io.run(app)
