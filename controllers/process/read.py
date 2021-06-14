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

@login_required
def read(processId):
    """ Performs a query to a process, process table or process table register based on the existence and value of GET parameters.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).

        Returns:
        res (dict): the requested process register, process table or process table register.
    """ 
    table_param = request.args.get("table")
    reg_id = request.args.get("reg_id")
    # query a process model 
    # TODO: filter by userid and column,value
    if table_param is None:
        try:
            res = Process.query.filter_by(id=processId).first_or_404()
        except SQLAlchemyError as e:
            error = str(e)
            return error 
        return res
    else:
        # query a table
        if reg_id is None:

        # query a table register
        else:


        # generate list of registers
        # TODO: filter by column,value
        # TODO: validate if the table name is valid 
        # TODO: validate if the table is in the process tables array
        # TODO: declare automap base class
        Base = automap_base()
        #update metadata and tables
        Base.prepare(db.engine, reflect=True)
        register_model = eval("Base.classes." + table_param)
        # perform query
        res=db.session.query(register_model).all()
        return [as_dict(c) for c in res]

    return res.as_dict()
    
