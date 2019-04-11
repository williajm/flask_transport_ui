"""
blah
"""
from dataclasses import dataclass
import json
import logging
from typing import List
import requests
from config import config

log = logging.getLogger(__name__)
session = requests.session()
session.params = config.get('auth')


@dataclass()
class Train:
    aimed_departure_time: str
    expected_departure_time: str
    destination_name: str
    platform: str
    operator_name: str
    origin_name: str
    status: str


class TrainEncoder(json.JSONEncoder):

    def default(self, obj):
        return obj.__dict__


def get_train_live(station: str) -> str:
    """
    blah
    :param station:
    :return:
    """
    url = f'http://transportapi.com/v3/uk/train/station/{station}/live.json'
    log.debug(f'GETing {url}')
    resp = session.get(url)
    if resp.status_code != requests.codes.ok:
        log.warning(f'http status={resp.status_code} for {url}')
        return '' # TODO throw an exception
    sanitised_obj = _sanitise(resp.text)
    sanitised_json = json.dumps(sanitised_obj, indent=4, cls=TrainEncoder)
    log.debug(f'sanitised_json={sanitised_json}')
    return sanitised_json


def _sanitise(query_result: str) -> List[Train]:
    query_json = json.loads(query_result)
    departures = query_json.get('departures', {}).get('all', [])
    trains = []
    for departure in departures:
        train = Train(aimed_departure_time=departure.get('aimed_departure_time'),
                      expected_departure_time=departure.get('expected_departure_time'),
                      destination_name=departure.get('destination_name'),
                      platform=departure.get('platform'),
                      operator_name=departure.get('operator_name'),
                      origin_name=departure.get('origin_name'),
                      status=departure.get('status'))
        trains.append(train)
    return trains
