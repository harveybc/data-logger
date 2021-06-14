""" Controller for the process/read endpoint.
    Description: Contains API endpoint handler functions for for reading individual process, process table or process table register.
"""

from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from controllers.common import as_dict, is_num
from models.process import Process
from flask import request

@login_required
def read(processId):
    """ Performs a query to a process, process table or process table register based on the existence and value of GET parameters.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).

        Returns:
        res (dict): the requested process register, process table or process table register.
    """ 
    process_param = request.args.get("process_id")
    # generate the list of processes 
    # TODO: filter by userid and column,value
    if process_param is None:
        try:
            res = Process.query.filter_by(id=processId).first_or_404()
        except SQLAlchemyError as e:
            error = str(e)
            return error
    # empty pass
    res.password=""
    return res.as_dict()
    
