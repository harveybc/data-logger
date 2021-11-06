echo "This script is made to be executed from the data_logger's root directory."
set PREV_PYTHONPATH = %PYTHONPATH%
set PYTHONPATH=%PYTHONPATH%;.\;\controllers;.
set FLASK_APP=app\migrate.py
set FLASK_ENV=development
flask run 
set PYTHONPATH=%PREV_PYTHONPATH%
 