""" Controller for the process table endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""
from sqlalchemy.ext.automap import automap_base
from app.app import db, Base

def init():
    #update metadata and tables
    db.Model.metadata.reflect(bind=db.engine)
    # reflect the tables
    Base.prepare(db.engine, reflect=False)

def read_all():
    init()
    try:
        res = Process.query.all()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # convert to list of dicts and empty pass
    res2 =[]
    for r in res:
        r.password = ""
        res2.append(as_dict(r))
    return res2