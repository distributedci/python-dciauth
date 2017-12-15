#!/usr/bin/env bash
set -eux
nohup python tests/e2e/server.py > /dev/null 2>&1 &
PID=$!
sleep 1
python tests/e2e/client.py
kill ${PID}
sleep 1