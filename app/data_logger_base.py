# -*- coding: utf-8 -*-
""" This File contains the DataLogger class, has methods for listing and loading plugins and execute their entry point. """

import argparse
import sys
import logging
import csv
import pkg_resources

# from feature_extractor import __version__

__author__ = "Harvey Bastidas"
__copyright__ = "Harvey Bastidas"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class DataLoggerBase():
    """ Base class For DataLogger. """
    
    def __init__(self, conf):
        """ Initializes DataLoggerBase with the configuration loaded from a JSON file. 
        Args:
        conf (JSON): plugin configuration loaded from configuration file.
        """
        self.conf = conf
        if conf != None:         
            self.setup_logging(logging.DEBUG) 
            _logger.debug(" * Creating data_logger instance...")
            # list available plugins
            if 'list_plugins' in conf:
                if self.conf['list_plugins'] == True:
                    _logger.debug("Listing plugins.")
                    self.find_plugins()
                    _logger.debug("Printing plugins.")
                    self.print_plugins()
            # set default plugin values if not found on config and execute core operations
            else:
                # sets default values for plugins
                if 'core_plugin' not in conf: 
                    self.conf['core_plugin'] = "core_basic_auth"
                    _logger.debug("Warning: core plugin not found in config file, using core_basic_auth")
                if 'store_plugin' not in conf: 
                    self.conf['store_plugin'] = "store_sqlite"  
                    _logger.debug("Warning: store plugin not found, using store_sqlite")
                if 'gui_plugin' not in conf: 
                    self.conf['gui_plugin'] = None
                    _logger.debug("* Warning: gui plugin not found")
                # execute core operations
                self.core()

    def core(self):
        """ Core feature_extractor operations. """
        _logger.debug("* Finding Plugins.")
        self.find_plugins()
        _logger.debug("* Loading plugins.")
        self.load_plugins() 
        if self.conf['core_plugin'] != None:
            _logger.debug("Setting up store plugin" )
            self.input_ds = self.ep_input.load_data() 
            _logger.debug("Performing core operations from the  core plugin.")
            self.output_ds = self.ep_core.core(self.input_ds) 
            _logger.debug("Executing the output plugin.")
            self.ep_output.store_data(self.output_ds) 
            _logger.info("feature_extractor finished.")
        else:
            exit('Error: No core plugin loaded.')
            
    
    def setup_logging(self, loglevel):
        """Setup basic logging.
        Args:
        loglevel (int): minimum loglevel for emitting messages
        """
        logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
        logging.basicConfig(
            level=loglevel,
            stream=sys.stdout,
            format=logformat,
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    
   


        