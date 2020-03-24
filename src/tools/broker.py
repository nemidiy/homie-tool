import copy

import base64
import sys
import math

from typing import Callable, Any, Dict

from hashlib import md5

import paho.mqtt.client as mqtt


class HomieMQTTBrokerClient:
    def __init__(self, client: mqtt.Client, **kwargs: Dict[str, str]):
        self.arguments = copy.deepcopy(kwargs)
        self.broker_username = self.arguments.get("broker_username", None)
        self.broker_password = self.arguments.get("broker_password", None)
        self.broker_tls_cacert = self.arguments.get("broker_tls_cacert", None)
        self.broker_host = self.arguments["broker_host"]
        self.broker_port = self.arguments["broker_port"]
        self.client = client

    def connect(
        self,
        cb_connect: Callable[[mqtt.Client, int], None],
        cb_message: Callable[[mqtt.Client, mqtt.MQTTMessage], None],
    ) -> None:

        self.client.on_connect = HomieMQTTBrokerClient.on_connect
        self.client.on_message = HomieMQTTBrokerClient.on_message

        # set username and password if given
        if self.broker_username and self.broker_password:
            self.client.username_pw_set(self.broker_username, self.broker_password)

        if self.broker_tls_cacert:
            self.client.tls_set(ca_certs=self.broker_tls_cacert)

        # save data to be used in the callbacks
        self.client.user_data_set(
            {"callback_connect": cb_connect, "callback_message": cb_message,}
        )

        self.client.connect(self.broker_host, self.broker_port, 60)

    def loop(self) -> None:
        # Blocking call that processes network traffic,
        # dispatches callbacks and handles reconnecting.
        self.client.loop_forever()

    @staticmethod
    def on_connect(
        client: mqtt.Client, userdata: Dict[str, Any], flags: Any, rc: int
    ) -> None:
        if rc != 0:
            print("Connection Failed with result code {}".format(rc))
            client.disconnect()
        else:
            print("Connected with result code {}".format(rc))
        userdata["callback_connect"](client, rc)

    @staticmethod
    def on_message(
        client: mqtt.Client, userdata: Dict[str, Any], msg: mqtt.MQTTMessage
    ) -> None:
        userdata["callback_message"](client, msg)
