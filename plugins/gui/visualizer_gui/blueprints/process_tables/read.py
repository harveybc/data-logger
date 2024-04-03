# endpoint index functions
from sqlalchemy.exc import SQLAlchemyError
import json
from app.util import as_dict
import math
from sqlalchemy import func, asc, desc

# returns a a row with id = id from the table table['name]
def read_data(db, Base, process, table, id):
    try:
        res = db.session.query(Base.classes[table['name']]).filter(Base.classes[table['name']]["id"] == id).one()
        res_map = map(as_dict, res)
    except SQLAlchemyError as e:
        error = str(e)
        print("1SQLAlchemyError : " , error)
        return error
    except Exception as e:
        error = str(e)
        print("Error : " ,error)
        return error
    
