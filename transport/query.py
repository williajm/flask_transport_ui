"""
Interfaces with the transport api search methods.
"""
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

import requests
from cachetools import TTLCache, cached

log = logging.getLogger(__name__)
session = requests.session()
session.params = {
    "app_id": os.getenv("ftu_app_id"),
    "app_key": os.getenv("ftu_app_key"),
}


@dataclass()
class Train:
    """
    Encapsulates the information that we want to display.
    """

    aimed_departure_time: str
    expected_departure_time: str
    destination_name: str
    platform: str
    operator_name: str
    origin_name: str
    status: str


class TrainEncoder(json.JSONEncoder):
    """
    Makes Train objects JSON encodable.
    """

    def default(self, o):
        return o.__dict__


@cached(cache=TTLCache(maxsize=1024, ttl=300))
def get_train_live(station: str) -> str:
    """
    Query transport API for the live departure times.
    :param station:
    :return:
    """
    url = f"http://transportapi.com/v3/uk/train/station/{station}/live.json"
    log.debug(f"GETing {url}")
    resp = session.get(url)
    if resp.status_code != requests.codes.ok:
        log.warning(f"http status={resp.status_code} for {url}")
        return ""
    trimmed_obj = _trim(resp.text)
    trimmed_json = json.dumps(trimmed_obj, indent=4, cls=TrainEncoder)
    log.debug(f"trimmed_json={trimmed_json}")
    return trimmed_json


def _trim(query_result: str) -> List[Train]:
    query_json = json.loads(query_result)
    departures = query_json.get("departures", {}).get("all", [])
    trains = []
    for departure in departures:
        train = Train(
            aimed_departure_time=departure.get("aimed_departure_time"),
            expected_departure_time=departure.get("expected_departure_time"),
            destination_name=departure.get("destination_name"),
            platform=departure.get("platform"),
            operator_name=departure.get("operator_name"),
            origin_name=departure.get("origin_name"),
            status=departure.get("status"),
        )
        trains.append(train)
    return trains


def get_train_fake(station: str) -> str:
    """
    Generates fake train data
    :param station:
    :return:
    """
    t = datetime.fromtimestamp(0)
    delta = timedelta(hours=1)
    trains = []
    for i in range(12):
        train = Train(
            aimed_departure_time=t.strftime("%H:%M"),
            expected_departure_time=t.strftime("%H:%M"),
            destination_name=f"{station} destination {i}",
            platform=str(i),
            operator_name=f"{station} operator",
            origin_name=f"{station} origin {i}",
            status=f'{"CANCELLED" if i % 3 == 0 else "ON TIME"}',
        )
        trains.append(train)
        t += delta
    return json.dumps(trains, indent=4, cls=TrainEncoder)
