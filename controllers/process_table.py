""" Controller for the process table endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""
from sqlalchemy.ext.automap import automap_base

def read_all():
    try:
        res = Process.query.all()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # convert to list of dicts and empty pass
    res2 =[]
    for r in res:
        r.password = ""
        res2.append(r.as_dict())
    return res2