# -*- coding: utf-8 -*-
"""
This File contains the LoadCSV class plugin. 
"""

import json

__author__ = "Harvey Bastidas"
__copyright__ = "Harvey Bastidas"
__license__ = "mit"

class SqliteStore(): 
    """ input plugin for the FeatureExtractor class, after initialization, the input_ds attribute is set """

    def __init__(self, conf):
        """ Initializes PluginBase. Do NOT delete the following line whether you have initialization code or not. """
        super().__init__(conf)
        # Insert your plugin initialization code here.
        pass
        
    def get_config_dict(self):
        """  Returns the config dict from this plugin's config.py """
        pass
    
    #Imported methods
    #from ._dashboard import load_data, get_user_id, get_max, get_count, get_column_by_pid, get_columns, get_users, get_user_by_username, get_processes, get_process_by_pid, processes_by_uid
    #from ._user import user_create

