# -*- encoding: utf-8 -*-
"""
This File contains the BasicAuthCore class plugin that implements a Connexion Flask-Sqlalchemy AAA API with basic authentication.
"""

import json
import logging
from .models.user import User
from .models.authorization import Authorization
from .models.log import Log
from .models.process import Process
import os
from .models.seeds.user import seed as u_seed

__author__ = "Harvey Bastidas"
__copyright__ = "Harvey Bastidas"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class BasicAuthCore(): 
    """ core plugin for the DataLogger class """

    def __init__(self, conf):
        """ assign configuration params as class attributes """
        # Insert your plugin initialization code here.
        _logger.debug("Initializing SqliteStore plugin")
        self.conf = conf
        self.specification_dir = os.path.dirname(__file__)
        self.specification_filename = 'DataLogger-OAS.apic.yaml'
        self.User = User
        self.Authorization = Authorization
        self.Log = Log 
        self.Process = Process
        # seed initial user 
    
    def user_seed(self, app, db):
        u_seed(app,db)

        

