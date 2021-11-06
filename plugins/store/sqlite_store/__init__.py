# -*- coding: utf-8 -*-
"""
This File contains the SqliteStore class plugin that allows data_logger to use a sqlite database. 
"""

import json
from .config import config_dict
import logging
from sqlalchemy.exc import SQLAlchemyError

__author__ = "Harvey Bastidas"
__copyright__ = "Harvey Bastidas"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class SqliteStore(): 
    """ input plugin for the FeatureExtractor class, after initialization, the input_ds attribute is set """

    def __init__(self, conf):
        """ assign configuration params as class attributes """
        # Insert your plugin initialization code here.
        _logger.info("Initializing store plugin")
        self.conf = conf
        
    def get_config_dict(self):
        """  Returns the config dict from this plugin's config.py """
        _logger.debug("SqliteStore plugin connecting with data_logger app")
        return config_dict
    
    

    #Imported methods
    #from ._dashboard import load_data, get_user_id, get_max, get_count, get_column_by_pid, get_columns, get_users, get_user_by_username, get_processes, get_process_by_pid, processes_by_uid
    #from ._user import user_create

