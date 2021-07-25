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
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from copy import deepcopy

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
        """ Populate starting user table
        Args:
        app (Flask): the current flask app object.
        db  (SQLAlchemy) : SQLAlchemy object
        """ 
        u_seed(app,db)

    def create_process(self, app, db, process):
        """ Create a register in the process table if another with the same name does not exist.
            Args:
            app (Flask): the current flask app instance.
            db (SQLAlchemy) : SQLAlchemy instance
            process (dict): process parameters

            Returns:
            new_process.id (int): the id of the new process or -1 if the process already exists
        """ 
        # Check if a process with the same name exists
        with app.app_context():
            db.session = scoped_session(sessionmaker(bind=db.engine, expire_on_commit=False))
            try:
                p = Process.query.filter_by(name=process["name"]).one()
                db.session.close()
            except SQLAlchemyError as e:
                p = None
            # Create the new process
            if p is None:
                process = deepcopy(process)
                process["tables"] = json.dumps(process["tables"]).replace("a","X")
                new_process = Process(**process) 
                db.session.add(new_process)
                db.session.commit()
                db.session.close()
                return new_process.id
            else:
                return -1

    def create_table(self, app, db, process_id, table):
        """ Create a table if another with the same name does not exist.
            Args:
            app (Flask): the current flask app instance.
            db (SQLAlchemy) : SQLAlchemy instance
            process_id (Integer): id of the process for which the table will be created
            table (dict): table parameters
        """
        # verify if the table already exists
        try:
           table_exists = db.engine.dialect.has_table(db.engine, table["name"])
        except SQLAlchemyError as e:
            table_exists = True
        # Create the new table
        if not table_exists:
            with app.app_context():
                table = deepcopy(table)
                #table["columns"]= json.dumps(table["columns"])
                new_table = ProcessTable(**table)
                if not db.engine.dialect.has_table(db.engine, new_table.name):
                    new_table.table.create(db.engine)
                #update metadata and tables
                db.Model.metadata.reflect(bind=db.engine)
                # reflect the tables
                Base = automap_base()
                Base.prepare(db.engine, reflect=True)
            
    

        

