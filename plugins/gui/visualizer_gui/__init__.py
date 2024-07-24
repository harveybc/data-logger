# -*- encoding: utf-8 -*-
"""
This File contains the Visualizer class plugin that implements static file serving for the current core plugin (sqlalchemy-flask app), to be used as its GUI.
"""
import json
import logging
import os
from importlib import import_module
from app.util import load_plugin_config

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
        self.static_url_path = '/plugins/gui/visualizer_gui'
    
    # register blueprints for plugin gui    
    def register_blueprints(self, app, core_ep, store_ep, db, Base):
        """ create the blueprints with all routes of the gui """
        for module_name in ('base', 'dashboard','user', 'process', 'util', 'evaluator'):
            module = import_module('plugins.gui.visualizer_gui.blueprints.{}'.format(module_name))
            bp = module.new_bp(self.template_path(), core_ep, store_ep, db, Base)
            app.register_blueprint(bp)
        """ create the blueprints with all routes of the gui for process tables """
        module = import_module('plugins.gui.visualizer_gui.blueprints.process_bp_factory')
        p_config = load_plugin_config()
        p_config_store = p_config["store"]
        processes = p_config_store["store_plugin_config"]["processes"]
        for process in processes:
            for table in process["tables"]:
                new_bp = module.ProcessBPFactory(process, table)
                bp = new_bp(self.template_path(), core_ep, store_ep, db, Base)
                app.register_blueprint(bp)
        
    
    def template_path(self):
        """ return this module's path """
        return os.path.dirname(__file__)

    
            
        

