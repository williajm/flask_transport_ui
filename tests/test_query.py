"""
Unit tests for query.py
"""
import json
import pytest
from transport.query import Train, TrainEncoder


def test_train_encodable():
    """
    Train should only be encodable when TrainEncoder is provided
    """
    train = Train(aimed_departure_time='10:26',
                  expected_departure_time='10:32',
                  destination_name='Westbury',
                  platform='4',
                  operator_name='Great Western Railway',
                  origin_name='Portsmouth Harbour',
                  status='LATE')
    with pytest.raises(TypeError):
        json.dumps(train)
    json.dumps(train, cls=TrainEncoder)
