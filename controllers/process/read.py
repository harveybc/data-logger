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
    

def update(processId, body):
    """ Update a register in db based on a json from a request's body parameter.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created process register with empty password field.
    """
    # query the existing register
    try:
        res = Process.query.filter_by(name=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # replace model with body fields
    body['id']=res.id
    res.__dict__ = body
    # perform update 
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # test if the model was updated 
    try:
        res = Process.query.filter_by(name=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # empty pass
    res.password=""
    # return register as dict
    return res.as_dict()

def delete(processId):
    """ Delete a register in db based on the id field of the process model, obtained from a request's processId url parameter.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).

        Returns:
        res (int): the deleted register id field
    """ 
    try:
        res = Process.query.filter_by(name=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # perform delete 
    db.session.delete(res)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    return res.id

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

def as_dict(model):   
        r2 = {}
        for c in model.__table__.columns:
            attr = getattr(model, c.name)
            if is_num(attr):
                r2[c.name]=attr
            else:
                r2[c.name]=str(attr)
        return r2

def is_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False
            