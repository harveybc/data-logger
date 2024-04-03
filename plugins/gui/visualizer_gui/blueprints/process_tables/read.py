# endpoint index functions
from sqlalchemy.exc import SQLAlchemyError
import json
from app.util import as_dict
import math
from sqlalchemy import func, asc, desc

# returns a a row with id = id from the table table['name]
def read_data(db, Base, process, table, id):
    try:
        table_name = table['name']
        print("table['name'] : ", table['name'])
        res = db.session.query(Base.classes.table_name).filter(Base.classes.table_name.id == id).one()
        res_map = as_dict(res)
        return json.dumps(res_map, default=str)
    except SQLAlchemyError as e:
        error = str(e)
        print("SQLAlchemyError : " , error)
        return error
    except Exception as e:
        error = str(e)
        print("Error : " ,error)
        return error
    
