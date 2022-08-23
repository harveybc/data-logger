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
        _logger.info("Initializing gui plugin")
        self.conf = conf
        # path for static files .//base/static
        self.static_url_path = self.template_path()+'/static/assets'
    
    # register blueprints for gui    
    def register_blueprints(self, app, core_ep, store_ep, db):
        """ create the blueprints with all routes of the gui """
        for module_name in ('base', 'dashboard', 'user', 'process', 'util'):
            module = import_module('plugins.gui.visualizer_gui.blueprints.{}'.format(module_name))
            bp = module.new_bp(self.template_path(), core_ep, store_ep, db)
            app.register_blueprint(bp)
    
    def template_path(self):
        """ return this module's path """
        return os.path.dirname(__file__)

    
            
        

