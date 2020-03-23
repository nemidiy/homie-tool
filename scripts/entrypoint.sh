#!/usr/bin/env bash

case "$1" in
    test)
        echo "teta"
        pytest
        ;;
    *)
        # The command is something like bash. Just run it in the right environment.
        exec "$@"
        ;;
esac

