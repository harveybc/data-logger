# -*- encoding: utf-8 -*-
"""
This File contains the Visualizer class plugin that implements static file serving for the current core plugin (sqlalchemy-flask app), to be used as its GUI.
"""
import json
import logging
import os
from importlib import import_module
from .blueprints.dashboard import dashboard_bp
from .blueprints.user import user_bp
from .blueprints.process import process_bp



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
        # path for static files .//base/static
        self.static_url_path = '/plugins/gui/visualizer_gui/base/static'
        self.dashboard_bp = dashboard_bp
        self.user_bp = user_bp
        self.process_bp = process_bp
        #self.process_table_bp = process_table_bp
        #self.authorization_bp = authorization_bp
        #self.log_bp = log_bp        
    # register blueprints for gui
    def register_blueprints(self, app):
        for module_name in ('base', 'home'):
            module = import_module('plugins.gui.visualizer_gui.{}.routes'.format(module_name))
            app.register_blueprint(module.blueprint)
    
    def template_path(self):
        """ return this module's path """
        return os.path.dirname(__file__)
            
        

