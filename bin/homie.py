import argparse
import sys

from typing import Callable, Any, Dict

import paho.mqtt.client as mqtt

from tools.broker import HomieMQTTBrokerClient

def add_common_arguments(parser: argparse.ArgumentParser ) -> None:
    parser.add_argument('-l', '--broker-host', type=str, required=False,
            help='host name or ip address of the mqtt broker', default="127.0.0.1")
    parser.add_argument('-p', '--broker-port', type=int, required=False,
            help='port of the mqtt broker', default=1883)
    parser.add_argument('-u', '--broker-username', type=str, required=False,
            help='username used to authenticate with the mqtt broker')
    parser.add_argument('-d', '--broker-password', type=str, required=False,
            help='password used to authenticate with the mqtt broker')
    parser.add_argument('-t', '--base-topic', type=str, required=False,
            help='base topic of the homie devices on the broker', default="homie/")
    parser.add_argument('-k', '--psk-key', type=str, required=False,
            help='psk key for TLS')
    parser.add_argument('-w', '--psk-value', type=str, required=False,
            help='psk value for TLS')
    parser.add_argument('--broker-tls-cacert', default=None, required=False,
            help='CA certificate bundle used to validate TLS connections. ' \
            'If set, TLS will be enabled on the broker conncetion')

def list_comm() -> None:
    parser = argparse.ArgumentParser(description=
                'lists all devices that support OTA at the broker')
    add_common_arguments(parser)
    args = parser.parse_args(sys.argv[2:])
    kwargs = dict(args._get_kwargs())

    devices : Dict[str, Any]= {}

    cli = mqtt.Client()
    b = HomieMQTTBrokerClient(cli, **kwargs)

    def on_connect(client: mqtt.Client, rc: int) -> None:
        topic = f"{kwargs['base_topic']}/+/$implementation/#"
        print(f"subscribing to {topic}")
        client.subscribe(topic)

    def on_message(client: mqtt.Client, message: mqtt.MQTTMessage) -> None:
        try:
            print(f"dup {message.dup}")
            print(f"info {message.info}")
            print(f"mid {message.mid}")
            print(f"payload {message.payload}")
            print(f"qos {message.qos}")
            print(f"retain {message.retain}")
            print(f"state {message.state}")
            print(f"ts {message.timestamp}")
            print(f"topic {message.topic}")
            print("----------------------")
        except Exception as e:
            print(e)
        return True
    
    b.connect(on_connect, on_message)
    b.loop()


def push_comm() -> None:
    parser = argparse.ArgumentParser(description=
                'push a firmware update to one or more devices')
    add_common_arguments(parser)
    args = parser.parse_args(sys.argv[2:])
    kwargs = dict(args._get_kwargs())
    cli = mqtt.Client()
    b = HomieMQTTBrokerClient(cli, **kwargs)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='ota firmware update tool for the Homie mqtt IoT convention.')

    parser.add_argument('command', help='commands available are list and push')
    args = parser.parse_args(sys.argv[1:2])

    func_name = f'{args.command}_comm'
    locals()[func_name]()