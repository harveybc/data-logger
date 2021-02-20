export FLASK_APP=run.py
export FLASK_ENV=development
export PREV_PYTHONPATH=$PYTHONPATH
export PYTHONPATH=$PYTHONPATH:./:/controllers
flask run
export PYTHONPATH=$PREV_PYTHONPATH
