import connexion
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

# Drops db
print("Dropping database")
db.drop_all(app=app.app)
drop_everything(db.engine)
print("done.")
# add the core plugin directory to the sys path
sys.path.append(data_logger.core_ep.specification_dir)
# import user, authorization, log and process models from core plugin 
from models.user import User
from models.process import Process
from models.authorization import Authorization
from models.log import Log
#Authorization = data_logger.core_ep.Authorization
#Log = data_logger.core_ep.Log
#Process = data_logger.core_ep.Process
print("Creating database")
db.create_all()
print("Seeding database with test user")
#from models.seeds.user import seed
# user seed function from core plugin       
data_logger.core_ep.user_seed(app.app, db)
# TODO: REMOVE UP TO HERE
# reflect the tables
db.Model.metadata.reflect(bind=db.engine)
Base.prepare(db.engine, reflect=False)
# Initialize data structure if does not exist
data_logger.store_ep.init_data_structure(app.app, db, data_logger.core_ep)