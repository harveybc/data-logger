""" Controller for the process endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""

from app.app import db
import json
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required
from app.app import login_manager
from ...models.process import Process
from ...models.process_table import ProcessTable
from ...models.process_register_factory import ProcessRegisterFactory
from sqlalchemy.ext.automap import automap_base
from flask import request
from ...controllers.common import as_dict, is_num
from ...controllers.authorization import authorization_required

@authorization_required
def read_all():
    """ Query all registers of the process, process table or process register.

        Returns:
        res (dict): the requested list.
    """ 
    # check if the "process" url param is set (either generate the list of tables or registers in a table) else, generate a list of processes
    process_param = request.args.get("process_id")
    # generate the list of processes 
    # TODO: filter by userid and column,value
    if process_param is None:
        try:
            res = Process.query.all()
        except SQLAlchemyError as e:
            error = str(e)
            return error
        # convert to list of dicts and empty pass
        res2 =[]
        for r in res:
            res2.append(as_dict(r))
        return res2
    # if the process url param is present, either generate a list of tables or a list of registers of a table
    else:
        table_param = request.args.get("table")
        # generate the list of tables 
        # TODO: filter by userid and column,value
        if table_param is None:
            res = ProcessTable.read_all(process_param)
            return res
        else:
            # generate list of registers
            # TODO: filter by column,value
            # TODO: validate if the table name is valid 
            # TODO: validate if the table is in the process tables array
            # TODO: declare automap base class
            ProcessRegister = ProcessRegisterFactory(table_param) 
            res = ProcessRegister.read_all(process_param, table_param)
            return res
