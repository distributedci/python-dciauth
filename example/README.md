# python-dciauth example

## requirements

    python -m pip install -Ur requirements.txt

## run tests

start server

    PYTHONPATH=$PYTHONPATH:.. FLASK_APP=server.py flask run

in another terminal test client

    PYTHONPATH=$PYTHONPATH:.. python client.py