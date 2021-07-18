# -*- coding: utf-8 -*-
""" This File contains the DataLogger class, has methods for listing and loading plugins and execute their entry point. """

import argparse
import sys
import logging
import csv
import pkg_resources
from app.data_logger_base import DataLoggerBase

# from data_logger import __version__

__author__ = "Harvey Bastidas"
__copyright__ = "Harvey Bastidas"
__license__ = "mit"

_logger = logging.getLogger(__name__)


class DataLogger(DataLoggerBase):
    """ Data Logger Plugin System """

    def __init__(self, store_conf, core_conf, gui_conf):
        """ Initializes DataLogger with the configuration loaded from JSON files. 
        Args:
        store_conf (JSON): store plugin configuration
        core_conf (JSON): core plugin configuration
        gui_conf (JSON): gui plugin configuration
        """         
        # set parameters as attributes
        self.store_conf = store_conf
        self.core_conf = core_conf
        self.gui_conf = gui_conf
        # setup stdout logging
        # TODO: Configurable stdout logging mode
        self.setup_logging(logging.DEBUG) 
        # list available plugins if required
        if ('list_plugins' in store_conf) or ('list_plugins' in core_conf) or ('list_plugins' in gui_conf):
            if self.conf['list_plugins'] == True:
                _logger.debug("Finding available plugins.")
                self.find_plugins()
                _logger.debug("Printing available plugins.")
                self.print_plugins()
        # sets default values for plugins
        if 'core_plugin' not in core_conf: 
            self.conf['core_plugin'] = "core_basic_auth"
            _logger.debug("Warning: core plugin not found in config file, using core_basic_auth")
        if 'store_plugin' not in store_conf: 
            self.conf['store_plugin'] = "store_sqlite"  
            _logger.debug("Warning: store plugin not found, using store_sqlite")
        if 'gui_plugin' not in gui_conf: 
            self.conf['gui_plugin'] = "gui_basic_auth"
            _logger.debug("* Warning: gui plugin not found, using core_basic_auth")
        _logger.debug("* Finding Plugins.")
        self.find_plugins()
        _logger.debug("* Loading plugins.")
        self.load_plugins() 
        if self.core_conf['core_plugin'] != None:
            #_logger.debug("Setting up store plugin" )
            #self.input_ds = self.ep_input.load_data() 
            _logger.debug("Performing core operations from the  core plugin.")
            #self.output_ds = self.ep_core.core(self.input_ds) 
            #_logger.debug("Executing the output plugin.")
            #self.ep_output.store_data(self.output_ds) 
            #_logger.info("feature_extractor finished.")
        else:
            print('Error: No core plugin loaded.')
            sys.exit()
    
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
