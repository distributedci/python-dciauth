#!/usr/bin/env bash
tox
export PYTHONPATH=${PYTHONPATH}:$(pwd)
export FLASK_APP='example/server.py'
nohup flask run > /dev/null 2>&1 &
PID=$!
sleep 1
python example/client.py > /dev/null
kill ${PID}
