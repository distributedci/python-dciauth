#!/usr/bin/env bash
nohup python -u tests/e2e/server.py > nohup.out 2>&1 &
PID=$!
sleep 1
python tests/e2e/client.py
TEST_RESULT=$?
cat nohup.out
if [ $TEST_RESULT -ne 0 ]; then
    rm nohup.out
    kill ${PID}
    exit 1
fi
rm nohup.out
kill ${PID}
sleep 1