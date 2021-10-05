echo "This Script is made to be executed from the data_logger's root directory."
set FLASK_APP=run.py
set FLASK_ENV=development
flask db_init 
