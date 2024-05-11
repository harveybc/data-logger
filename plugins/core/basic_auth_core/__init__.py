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


#from .models.process_register_factory import ProcessRegisterFactory
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from copy import deepcopy
from app.util import sanitize_str
from sqlalchemy import func
import warnings
# import controllers
from .controllers.configs import ConfigsController


import os

__author__ = "Harvey Bastidas"
__copyright__ = "Harvey Bastidas"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class BasicAuthCore(): 
    """ core plugin for the DataLogger class """

    def __init__(self, conf):
        """ assign configuration params as class attributes """
        # Insert your plugin initialization code here.
        _logger.info("Initializing core plugin")
        self.conf = conf
        self.specification_dir = os.path.dirname(__file__)
        self.specification_filename = conf['core_plugin_config']['filename']
        self.User = User
        self.Authorization = Authorization
        self.Log = Log 
        self.Process = Process
        self.ProcessTable = ProcessTable
        self.ConfigsController = ConfigsController
        self.Base = None
        # seed initial user 

    def seed_init_data(self, app, db):
        """ Populate starting user and process tables
        Args: 
        app (Flask): the current flask app object.
        db  (SQLAlchemy) : SQLAlchemy object
        """ 
        _logger.info("Seeding initial data")
        from .models.seeds.user import seed as user_seed
        from .models.seeds.process_table import seed as process_table_seed
        user_seed(app,db)
        # seeds training_error data
        process_table_seed(app,db, "fe_config")
        process_table_seed(app,db, "fe_training_error")

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
            db.session = scoped_session(sessionmaker(bind=db.engine, expire_on_commit=True))
            try:
                p = Process.query.filter_by(name=process["name"]).one()
                #db.session.expunge_all()
                #db.session.close()
            except SQLAlchemyError as e:
                p = None
            # Create the new process
            if p is None:
                process = deepcopy(process)
                process["tables"] = json.dumps(process["tables"]) 
                new_process = Process(**process) 
                db.session.add(new_process)
                db.session.commit()
                #db.session.expunge_all()
                #db.session.close()
                return new_process.id
            else:
                return -1

    def create_table(self, app, db, table):
        """ Create a table if another with the same name does not exist.
            Args:
            app (Flask): the current flask app instance.
            db (SQLAlchemy) : SQLAlchemy instance
            table (dict): table parameters
        """
        # verify if the table already exists
        try:
            insp = db.inspect(db.engine)
            table_exists = insp.has_table(table["name"])
        except SQLAlchemyError as e:  
            table_exists = True
            _logger.info("Error: %s", str(e))
        # Create the new table
        if not table_exists:
            with app.app_context(): 
                table = deepcopy(table)
                #table["columns"]= json.dumps(table["columns"])
                new_table = ProcessTable(**table)
                new_table.table.create(db.engine)
                #update metadata and tables
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    db.Model.metadata.reflect(bind=db.engine)
                    # reflect the tables
                    self.Base.prepare(db.engine, reflect=False)
    
    def init_data_structure(self, app, db, store_conf):
        """ Create the data structure (processes/tables) from the config_store.json """
        print("store_conf = ",store_conf)
        # create the processes table if it does not exists
        try:
            from .models.user import User
            from .models.authorization import Authorization
            from .models.log import Log
            from .models.process import Process

            db.create_all()
            _logger.info("Created fixed data structure tables:")
            for t in db.metadata.sorted_tables:
                _logger.info("  %s", t.name)
        except SQLAlchemyError as e:
            print(str(e))
        # create each process from the processes attribute
        _logger.info("Created configurable data structure tables:")
        for process in store_conf["store_plugin_config"]["processes"]:
            process_id = self.create_process(app, db, process)
            if process_id == -1:
                try:
                    Process = self.Process
                    with app.app_context():
                        p = Process.query.filter_by(name=process["name"]).one()
                    process_id == p.id
                except SQLAlchemyError as e:
                    p = None
            if process_id>-1:
                _logger.info("  Process %s tables:", process["name"])
                # create each table of the process
                for table in process["tables"]:
                    self.create_table(app, db, table)
                    _logger.info("      %s", table["name"])
            db.session.commit()

    def database_init(self, app, db, data_logger, store_conf):
        _logger = logging.getLogger(__name__)
        # initialize Database configuration
        from sqlalchemy.engine.reflection import Inspector
        from sqlalchemy.schema import (
            DropConstraint,
            DropTable,
            MetaData,
            Table,
            ForeignKeyConstraint,
        )
        con = db.engine.connect()
        trans = con.begin()
        inspector = Inspector.from_engine(db.engine)
        meta = MetaData()
        tables = []
        all_fkeys = []
        for table_name in inspector.get_table_names():
            fkeys = []
            for fkey in inspector.get_foreign_keys(table_name):
                if not fkey["name"]:
                    continue
                fkeys.append(ForeignKeyConstraint((), (), name=fkey["name"]))
            tables.append(Table(table_name, meta, *fkeys))
            all_fkeys.extend(fkeys)
        for fkey in all_fkeys:
            con.execute(DropConstraint(fkey))
        for table in tables:
            con.execute(DropTable(table))
        trans.commit()
        _logger.info("Database dropped")
        # create the data structure from the store plugin config file
        self.init_data_structure(app, db, store_conf)
        _logger.info("Data structure created")
        self.seed_init_data(app, db)
        _logger.info("Initial data seed done")
                