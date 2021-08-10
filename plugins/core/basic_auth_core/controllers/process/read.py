""" Controller for the process/read endpoint.
    Description: Contains API endpoint handler functions for for reading individual process, process table or process table register.
"""

from app.app import db 
import json
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from ...controllers.common import as_dict, is_num
from ...models.process import Process
from ...models.process_table import ProcessTable
from ...models.process_register import ProcessRegister

from flask import request
from sqlalchemy.ext.automap import automap_base
from ...controllers.authorization import authorization_required

@authorization_required
def read(process_id):
    """ Performs a query to a process, process table or process table register based on the existence and value of GET parameters.

        Args:
        process_id (str): id field of the process model, obtained from a request's process_id url parameter (processs/<process_id>).

        Returns:
        res (dict): the requested process register, process table or process table register.
    """ 
    table_param = request.args.get("table")
     
    # query a process model 
    # TODO: filter by userid and column,value
    if table_param is None:
        try:
            res = Process.query.filter_by(id=process_id).one().as_dict()
        except SQLAlchemyError as e:
            error = str(e)
            return error 
        return res
    else:
        # query a table
        reg_id = request.args.get("reg_id")
        if reg_id is None:
            res = ProcessTable.read(process_id, table_param)
            return res
        # query a table register
        else:
            # query a table register
            res = ProcessRegister.read(process_id, table_param, reg_id)
            return as_dict(res)
    #return res.as_dict()
    
