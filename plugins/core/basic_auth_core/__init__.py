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
from .models.process_table import ProcessTable
from .models.process_register import ProcessRegister
from sqlalchemy.ext.automap import automap_base

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
        self.specification_filename = conf['core_plugin_config']['filename']
        self.User = User
        self.Authorization = Authorization
        self.Log = Log 
        self.Process = Process
        self.ProcessTable = ProcessTable
        # seed initial user 
    
    def user_seed(self, app, db):
        u_seed(app,db)

    def create_process(self, db, process):
        new_process = Process(process)
        db.session.add(new_process)
        db.session.commit()
        return new_process.id

    def create_table(self, db, process_id, table):
        # instantiate process table with the body dict as kwargs
        new_table = ProcessTable(table)
        if not db.engine.dialect.has_table(db.engine, new_table.name):
            new_table.table.create(db.engine)
        #update metadata and tables
        db.Model.metadata.reflect(bind=db.engine)
        # reflect the tables
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)
        
    

        

