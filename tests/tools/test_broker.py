import sys

sys.path.append("src")

import pytest

from tools.broker import HomieMQTTBrokerClient


def test_dummy():
    c = HomieMQTTBrokerClient(None, **{"broker_host": "127.0.0.1", "broker_port": 1883})
