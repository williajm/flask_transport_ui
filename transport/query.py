"""
blah
"""
import logging
import json
import requests
from config import config

log = logging.getLogger(__name__)
session = requests.session()
session.params = config.get('auth')


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
    log.debug(json.dumps(json.loads(resp.text), indent=4))
    return resp.text
