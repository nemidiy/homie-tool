#!/usr/bin/env bash

case "$1" in
    test)
        mosquitto -c /mosquitto/mosquitto.conf -d
        pytest
        ;;
    *)
        # The command is something like bash. Just run it in the right environment.
        mosquitto -c /mosquitto/mosquitto.conf -d
        exec "$@"
        ;;
esac

