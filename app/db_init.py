from flask import Flask
import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from app.util import load_plugin_config
from app.data_logger import DataLogger
import sys
from decouple import config
from sqlalchemy.ext.automap import automap_base
import logging


def database_init(app, data_logger):
    _logger = logging.getLogger(__name__)
    # initialize Database configuration
    db = SQLAlchemy(app)
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
    data_logger.store_ep.init_data_structure(app, db, data_logger.core_ep)
    _logger.info("Data structure created")
    

# create command function

#def reset_db(db, data_logger):
#    # Drops db
#    print("Dropping database")
#    drop_everything(db.engine)
#    print("done.")
#    # add the core plugin directory to the sys path
#    sys.path.append(data_logger.core_ep.specification_dir)
#    print("Import core models")
#    # import user, authorization, log and process models from core plugin 
#    from models.user import User
#    #from models.process import Process
#    #from models.authorization import Authorization
#    #from models.log import Log
#    #data_logger.core_ep.UserFactory()
##    #data_logger.core_ep.AuthorizationFactory()
 #   #data_logger.core_ep.LogFactory()
 #   #data_logger.core_ep.import_models()

#    print("Creating database")
#    db.create_all()
    #print("Seeding database with test user")
    #from models.seeds.user import seed
    # user seed function from core plugin       
    #data_logger.core_ep.user_seed(app.app, db)
    # TODO: REMOVE UP TO HERE
    # reflect the tables
    #db.Model.metadata.reflect(bind=db.engine)
    #Base.prepare(db.engine, reflect=False)
    # Initialize data structure if does not exist
    #data_logger.store_ep.init_data_structure(app.app, db, data_logger.core_ep)
