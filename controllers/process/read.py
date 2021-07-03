""" Controller for the process/read endpoint.
    Description: Contains API endpoint handler functions for for reading individual process, process table or process table register.
"""

from app.app import db 
import json
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from controllers.common import as_dict, is_num
from models.process import Process
from flask import request
from sqlalchemy.ext.automap import automap_base

@authorization_required
def read(processId):
    """ Performs a query to a process, process table or process table register based on the existence and value of GET parameters.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).

        Returns:
        res (dict): the requested process register, process table or process table register.
    """ 
    table_param = request.args.get("table")
    # query a process model 
    # TODO: filter by userid and column,value
    if table_param is None:
        try:
            res = Process.query.filter_by(id=processId).first_or_404().as_dict()
        except SQLAlchemyError as e:
            error = str(e)
            return error 
        return res
    else:
        # parse the table_param string because eval is used
        table_param = table_param.strip("\"',\\*.!:-+/ #\{\}[]")
        # query a table
        reg_id = request.args.get("reg_id")
        if reg_id is None:
            try:
                # TODO: query table by name from process tables array 
                #ptable.read_all(int(process_param))
                proc = Process.query.filter_by(id=processId).first_or_404().as_dict()
                res_list = json.loads(proc["tables"])
            except SQLAlchemyError as e:
                error = str(e)
                return error
            # search for the name in the keys of elements of an the tables array.       
            try:
                return next(x for x in res_list if table_param in x["name"])
            except StopIteration:
                raise ValueError("No matching record found")     
            return res
        # query a table register
        else:
            # query a table register
            Base = automap_base()
            #update metadata and tables
            Base.prepare(db.engine, reflect=True)
            register_model = eval("Base.classes." + table_param)
            # perform query
            res=db.session.query(register_model).filter_by(id=reg_id).first_or_404()
            return as_dict(res)
    #return res.as_dict()
    
