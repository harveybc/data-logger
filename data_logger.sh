export PREV_PYTHONPATH=$PYTHONPATH
export $PYTHONPATH=$PYTHONPATH;.\
export FLASK_APP=run.py
flask run
export $PYTHON=$PREV_PYTHONPATH
