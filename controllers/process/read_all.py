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


def read_all():
    """ Query all registers of the process, process table or process register.

        Returns:
        res (dict): the requested process registers with empty password field.
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
            r.password = ""
            res2.append(r.as_dict())
        return res2
    # if the process url param is present, either generate a list of tables or a list of registers of a table
    else:
        table_param = request.args.get("table")
        # generate the list of tables 
        # TODO: filter by userid and column,value
        if table_param is None:
            try:
                # TODO: get tables array from the process
                #ptable.read_all(int(process_param))
                proc = Process.query.filter_by(id=int(process_param)).first_or_404()
                res = json.loads(proc.tables)
            except SQLAlchemyError as e:
                error = str(e)
                return error
            return res
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
