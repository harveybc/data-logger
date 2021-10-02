# -*- encoding: utf-8 -*-
""" DataLogger: Run script.
    Description: Initializes the plugin system and starts the application.
    This script is called by the command 'flask run' in the startup scripts 'data_logger.sh' and 'data_logger.bat', 
    where FLASK_APP env variable is set to 'run.py'(this script).
"""

from os import environ
from sys import exit
from decouple import config
from json import load as json_load
from json import dumps
from app.app import create_app, load_plugin_config
from app.data_logger import DataLogger

# load the plugin config files
plugin_conf = load_plugin_config()
# initialize plugin system
print(" * Creating data_logger instance...")
data_logger = DataLogger(plugin_conf['store'], plugin_conf['core'], plugin_conf['gui'])

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True)
# setup config mode
get_config_mode = 'Debug' if DEBUG else 'Production'
# load config from the config_dict according to the set config mode.
try:
    # load the config_dict from the store plugin entry point (instance of the selected store plugin's class)
    config_dict = data_logger.store_ep.get_config_dict()
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')
app = create_app( app_config, data_logger)

def print_spec():
    # read json
    spec = json_load(data_logger.core_ep.specification_dir+'/' + data_logger.core_ep.specification_filename)
    # dump json as string
    return dumps(spec)

