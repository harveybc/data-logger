""" Controller for the process endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""

from app.app import db
import json
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from datetime import datetime
from app.app import login_manager
from models.process import Process
from models.process_table import ProcessTable
from models.process_register import ProcessRegister
from sqlalchemy import Table, insert
from sqlalchemy.ext.automap import automap_base
from flask import request
import controllers.process_table as ptable

@login_required
def read(processId):
    """ Query a register in db based on the id field of the process model, obtained from a request's processId url parameter.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).

        Returns:
        res (dict): the requested process register with empty password field.
    """ 
    # if the 
    try:
        res = Process.query.filter_by(name=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # empty pass
    res.password=""
    return res.as_dict()
    
