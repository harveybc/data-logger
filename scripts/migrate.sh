echo "This Script is made to be executed from the data_logger's root directory."
export FLASK_APP=app/migrate.py
export FLASK_ENV=development
flask dbinit