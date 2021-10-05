from flask import Flask
import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from app.util import load_plugin_config
from app.data_logger import DataLogger
import sys
from decouple import config
from sqlalchemy.ext.automap import automap_base

# initialize flask app
app = Flask(__name__)
# initialize Database configuration
# load the plugin config files
plugin_conf = load_plugin_config()
# initialize plugin system
print(" * Creating data_logger instance...")
data_logger = DataLogger(plugin_conf['store'], plugin_conf['core'], plugin_conf['gui'])

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True)
# setup config mode
get_config_mode = 'Debug' if DEBUG else 'Production'
# load config from the config_dict according to the set config mode.
try:
    # load the config_dict from the store plugin entry point (instance of the selected store plugin's class)
    config_dict = data_logger.store_ep.get_config_dict()
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')


#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://db.sqlite3'
app.config.from_object(app_config)
# database
db = SQLAlchemy(app)
Base = automap_base()

def drop_everything(engine):
    """drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    from sqlalchemy.engine.reflection import Inspector
    from sqlalchemy.schema import (
        DropConstraint,
        DropTable,
        MetaData,
        Table,
        ForeignKeyConstraint,
    )
    con = engine.connect()
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

# create command function
@click.command(name='dbinit')
@with_appcontext
def dbinit():
    
    # Drops db
    print("Dropping database")
    drop_everything(db.engine)
    print("done.")
    # add the core plugin directory to the sys path
    sys.path.append(data_logger.core_ep.specification_dir)
    print("Import core models")
    # import user, authorization, log and process models from core plugin 
    from models.user import User
    #from models.process import Process
    #from models.authorization import Authorization
    #from models.log import Log
    #data_logger.core_ep.UserFactory()
    #data_logger.core_ep.AuthorizationFactory()
    #data_logger.core_ep.LogFactory()
    #data_logger.core_ep.import_models()

    print("Creating database")
    db.create_all()
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


# add command function to cli commands
app.cli.add_command(db_init)