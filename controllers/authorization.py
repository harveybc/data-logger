""" Controller for the log endpoints. 
    Description: Contains API endpoint handler functions for CRUD operations 
    on the logs table whose registers are an ordered set of rules
    that a request must approve to perform its intended action.
    
    By default, admin users can CRUD processes, tables and table registers.
    
    Also by default, all users can read/create registers on their processes' tables, 
    but can't create processes or tables, and can't update/delete registers.

    When logs are created for an user, process or a table
    the user, process or table is denied all access but the indicated.

    The list of logs for an user, process or table is ordered by the 
    priority column and the highest priority rules override the lowest priority ones.

"""

from app.app import db
import json
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from datetime import datetime
from app.app import login_manager
from models.log import Log
from models.process_table import ProcessTable
from models.process_register import ProcessRegister
from sqlalchemy.ext.automap import automap_base
from controllers.common import as_dict, is_num

@login_required
def create(body):
    """ Create a register in db based on a json from a request's body parameter.

        Args:
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created register.
    """
    # instantiate user with the body dict as kwargs
    new = Log(**body)
    # create new flask-sqlalchemy session
    db.session.add(new)
    try:
        db.session.commit()
        new_id =  new.id
        db.session.close()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # test if the new user was created 
    try:
        res = Log.query.filter_by(id=new_id).one()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # return register as dict
    return res.as_dict()

def read(log_id):
    """ Performs a query log register.

        Args:
        processId (str): log_id (log/<log_id>).

        Returns:
        res (dict): the requested  register.
    """
    try:
        res = Log.query.filter_by(id=log_id).one().as_dict()
    except SQLAlchemyError as e:
        error = str(e)
        return error 
    return res

def update(log_id, body):
    """ Update a register in db based on a json from a request's body parameter.

        Args:
        userId (str): id field of the model, obtained from url parameter (log/<log_id>).
        body (dict): dict containing the fields of the register, obtained from json in the body of the request.

        Returns:
        res (dict): the updated register
    """
     # query the existing register
    try:
        process_model = Log.query.filter_by(id=log_id).one()
        for property, value in body.items():
            setattr(process_model, property, value)
    except SQLAlchemyError as e:
        error = str(e)
        res = { 'error_a' : error}
    # replace model with body fields
    
    # perform update 
    try:
        db.session.commit()
        db.session.close()
    except SQLAlchemyError as e:
        error = str(e)
        res = { 'error_b' : error}
    # test if the model was updated 
    try:
        res = Log.query.filter_by(id=int(log_id)).one().as_dict()
        db.session.close()
    except SQLAlchemyError as e:
        error = str(e)
        res = { 'error_c' : error}
    return res

def delete(log_id):
    """ Delete a register in db based on the id field of the authorizarions model, obtained from a request's log_id url parameter.

        Args:
        processId (str): id field , obtained from a request's url parameter (log/<log_id>).

        Returns:
        res (int): the deleted register id field
    """
    try:
        res = Log.query.filter_by(id=log_id).one()
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

@login_required
def read_all():
    """ Query all registers of the logs table.

        Returns:
        res (dict): the requested list.
    """ 
    try:
        res = Log.query.all()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # convert to list of dicts and empty pass
    res2 =[]
    for r in res:
        res2.append(r.as_dict())
    return res2






