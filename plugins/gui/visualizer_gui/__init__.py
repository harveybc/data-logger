# -*- encoding: utf-8 -*-
"""
This File contains the Visualizer class plugin that implements static file serving for the current core plugin (sqlalchemy-flask app), to be used as its GUI.
"""
import json
import logging
import os

__author__ = "Harvey Bastidas"
__copyright__ = "Harvey Bastidas"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class Visualizer(): 
    """ gui plugin for the DataLogger class """

    def __init__(self, conf):
        """ assign configuration params as class attributes """
        # Insert your plugin initialization code here.
        _logger.debug("Initializing Visualizer gui plugin")
        self.conf = conf
        #self.specification_dir = os.path.dirname(__file__)
        #self.specification_filename = 'DataLogger-OAS.apic.yaml'
        #self.User = User
        #self.Authorization = Authorization
        #self.Log = Log 
        #self.Process = Process
        

