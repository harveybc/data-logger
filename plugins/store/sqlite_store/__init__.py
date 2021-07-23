# -*- coding: utf-8 -*-
"""
This File contains the SqliteStore class plugin that allows data_logger to use a sqlite database. 
"""

import json
from .config import config_dict
import logging

__author__ = "Harvey Bastidas"
__copyright__ = "Harvey Bastidas"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class SqliteStore(): 
    """ input plugin for the FeatureExtractor class, after initialization, the input_ds attribute is set """

    def __init__(self, conf):
        """ assign configuration params as class attributes """
        # Insert your plugin initialization code here.
        _logger.debug("Initializing SqliteStore plugin")
        self.conf = conf
        
    def get_config_dict(self):
        """  Returns the config dict from this plugin's config.py """
        _logger.debug("SqliteStore plugin connecting with data_logger app")
        return config_dict
    
    def init_data_structure(self, app, db, core_ep):
        """ Create the data structure (processes/tables) from the config_store.json """
        # create each process from the processes attribute
        for process in self.conf["store_plugin_config"]["processes"]:
            process_id = core_ep.create_process(app, db, process)
            # create each table of the process
            for table in process["tables"]:
                core_ep.crete_table(app, db, process_id, table)

    #Imported methods
    #from ._dashboard import load_data, get_user_id, get_max, get_count, get_column_by_pid, get_columns, get_users, get_user_by_username, get_processes, get_process_by_pid, processes_by_uid
    #from ._user import user_create

