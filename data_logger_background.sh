export FLASK_APP=run.py
export FLASK_ENV=development
export PREV_PYTHONPATH=$PYTHONPATH
export PYTHONPATH=$PYTHONPATH:./:/controllers
nohup flask run --host=0.0.0.0 --port=60500 > log.txt 2>&1 &
export PYTHONPATH=$PREV_PYTHONPATH
