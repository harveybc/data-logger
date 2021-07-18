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
    
    def find_plugins(self):
        """" Populate the discovered plugin lists """

        self.discovered_store_plugins = {
            entry_point.name: entry_point.load()
            for entry_point
            in pkg_resources.iter_entry_points('data_logger.store_plugins')
        }
        self.discovered_gui_plugins = {
            entry_point.name: entry_point.load()
            for entry_point
            in pkg_resources.iter_entry_points('data_logger.gui_plugins')
        }
        self.discovered_core_plugins = {
            entry_point.name: entry_point.load()
            for entry_point
            in pkg_resources.iter_entry_points('data_logger.core_plugins')
        }

    def load_plugins(self):
        """ Loads plugin entry points into class attributes"""
        for i in self.discovered_store_plugins:
            print(i, " => ", self.discovered_store_plugins[i])
        if self.store_conf['store_plugin'] in self.discovered_store_plugins:
            # entry point (plugin class) for plugin from discovered plugins
            self.s_ep = self.discovered_store_plugins[self.conf['store_plugin']]
            # instantiate plugin class defined in the setup.cfg [options.entry_points] section.
            self.store_ep = self.ep_s(self.store_conf)
        else:
            print("Error: Store Plugin not found. Use option list_plugins=True to show the list of available plugins.")
            sys.exit()
        if self.gui_conf['gui_plugin'] in self.discovered_gui_plugins:
            # entry point (plugin class) for plugin from discovered plugins
            self.g_ep = self.discovered_gui_plugins[self.gui_conf['gui_plugin']]
            # instantiate plugin class defined in the setup.cfg [options.entry_points] section.
            self.gui_ep = self.g_ep(self.gui_conf)
        else:
            print("Error: GUI Plugin not found. Use option list_plugins=True to show the list of available plugins.")
            sys.exit()
        if self.core_conf['core_plugin'] in self.discovered_core_plugins:
            # entry point (plugin class) for plugin from discovered plugins
            self.c_ep = self.discovered_core_plugins[self.core_conf['core_plugin']]
            # instantiate plugin class defined in the setup.cfg [options.entry_points] section.
            self.core_ep = self.c_ep(self.core_conf)
        else:
            print("Error: Core Plugin not found. Use option list_plugins=True to show the list of available plugins.")
            sys.exit()
    
    def print_plugins(self):
        print("Discovered input plugins:")
        for key in self.discovered_store_plugins:
            print(key+"\n")
        print("Discovered output plugins:")
        for key in self.discovered_gui_plugins:
            print(key+"\n")
        print("Discovered core plugins:")
        for key in self.discovered_core_plugins:
            print(key+"\n")
        


   


        