"""
Entry point module for the transport application.
"""
from importlib import resources
import json
import logging
import logging.config
from transport import query


def configure_logging():
    """
    blah
    :return:
    """
    with resources.open_text('config', 'logging.json') as log_config:
        logging.config.dictConfig(json.load(log_config))


if __name__ == "__main__":
    configure_logging()
    log = logging.getLogger()
    result = query.get_train_live('SOU')
