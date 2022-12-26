set FLASK_APP=run.py
set FLASK_ENV=development
set PREV_PYTHONPATH = %PYTHONPATH%
set PYTHONPATH=%PYTHONPATH%;.\;\controllers;.
flask run --host=127.0.0.1 --port 60500
set PYTHONPATH=%PREV_PYTHONPATH%