echo "This Script is made to be executed from the data_logger's root directory."
export PREV_PYTHONPATH=$PYTHONPATH
export PYTHONPATH=$PYTHONPATH:./:/controllers
export FLASK_APP=app/migrate.py
export FLASK_ENV=development
flask dbinit
export PYTHONPATH=$PREV_PYTHONPATH