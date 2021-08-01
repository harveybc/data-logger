# -*- encoding: utf-8 -*-
"""
This File contains the Visualizer class plugin that implements static file serving for the current core plugin (sqlalchemy-flask app), to be used as its GUI.
"""
import json
import logging
import os
from importlib import import_module

__author__ = "Harvey Bastidas"
__copyright__ = "Harvey Bastidas"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class VisualizerGui(): 
    """ gui plugin for the DataLogger class """

    def __init__(self, conf):
        """ assign configuration params as class attributes """
        # Insert your plugin initialization code here.
        _logger.info("Initializing VisualizerGui plugin")
        self.conf = conf
        # rel_path = os.path.relpath(os.path.dirname(__file__) )
        #print("abspath=", os.path.abspath(__file__) +'/base/static')
        #print("commonpath=", os.path.commonpath(__file__))
        #print("basename=", os.path.basename(__file__) +'/base/static')
        #print("relpath=", os.path.relpath(os.curdir, start=os.curdir))
        # path for static files .//base/static
        self.static_url_path = os.path.abspath(__file__)+'plugins/gui/visualizer_gui/base/static'
        #self.specification_dir = os.path.dirname(__file__)
        #self.specification_filename = 'DataLogger-OAS.apic.yaml'
        #self.User = User
        #self.Authorization = Authorization
        #self.Log = Log 
        #self.Process = Process
        
    # register blueprints for gui
    def register_blueprints(self, app):
        for module_name in ('base', 'home'):
            module = import_module('plugins.gui.visualizer_gui.{}.routes'.format(module_name))
            app.register_blueprint(module.blueprint)
        

