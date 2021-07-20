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
from .models.authorization import Authorization
from .models.process_table import ProcessTable
from .models.process_register import ProcessRegister
from sqlalchemy.ext.automap import automap_base
from .controllers.common import as_dict, is_num
from functools import wraps
from flask import (current_app)
from flask import request

def authorization_required(func):
    """ This decoration indicates that the decorated function should verify if the current user is authorized for the current request.

        Args:
        func (function): The function to be decorated

        Returns:
        res (dict): func if the user is authorized, login_manager.unauthorized() 
    """
    @wraps(func)
    @login_required
    def decorated_view(*args, **kwargs):
        if is_authorized(*args, **kwargs):
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()
    return decorated_view

from .controllers.log import log_required

@authorization_required
@log_required
def create(body):
    """ Create a register in db based on a json from a request's body parameter.

        Args:
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created register.
    """
    # instantiate user with the body dict as kwargs
    new = Authorization(**body)
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
        res = Authorization.query.filter_by(id=new_id).one()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # return register as dict
    return res.as_dict()

@authorization_required
def read(authorization_id):
    """ Performs a query log register.

        Args:
        process_id (str): authorization_id (log/<authorization_id>).

        Returns:
        res (dict): the requested  register.
    """
    try:
        res = Authorization.query.filter_by(id=authorization_id).one().as_dict()
    except SQLAlchemyError as e:
        error = str(e)
        return error 
    return res

@authorization_required
@log_required
def update(authorization_id, body):
    """ Update a register in db based on a json from a request's body parameter.

        Args:
        userId (str): id field of the model, obtained from url parameter (log/<authorization_id>).
        body (dict): dict containing the fields of the register, obtained from json in the body of the request.

        Returns:
        res (dict): the updated register
    """
     # query the existing register
    try:
        process_model = Authorization.query.filter_by(id=authorization_id).one()
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
        res = Authorization.query.filter_by(id=int(authorization_id)).one().as_dict()
        db.session.close()
    except SQLAlchemyError as e:
        error = str(e)
        res = { 'error_c' : error}
    return res

@authorization_required
@log_required
def delete(authorization_id):
    """ Delete a register in db based on the id field of the authorizarions model, obtained from a request's authorization_id url parameter.

        Args:
        process_id (str): id field , obtained from a request's url parameter (log/<authorization_id>).

        Returns:
        res (int): the deleted register id field
    """
    try:
        res = Authorization.query.filter_by(id=authorization_id).one()
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

@authorization_required
def read_all():
    """ Query all registers of the logs table.

        Returns:
        res (dict): the requested list.
    """ 
    try:
        res = Authorization.query.all()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # convert to list of dicts and empty pass
    res2 =[]
    for r in res:
        res2.append(r.as_dict())
    return res2

def is_authorized(*args, **kwargs):
    """ Verify if a request is authorized for the current user.
        
        Args:
        process_id (int): the id of the process for authorization

        Returns:
        res (dict): true if the user is authorized for the request 
    """ 
    method = request.method
    route = request.path
    get_params = request.args
    body_params = request.json
    # find process_id from args
    # if args[0] is None(read_all controller), process_id = request.args.get("process_id")
    print("args" , args)
    print("kwargs" , kwargs)
    process_id = None
    if len(kwargs) > 0:
        if "process_id" in kwargs:
            process_id = kwargs["process_id"]
        # if args[0] is a dict (update controller), if table is in args[0], process_id = args[0]['table']['process_id'], else process_id =  args[0]['register']['process_id']
        elif "body" in kwargs:
            if "table" in kwargs["body"]:
                if isinstance(kwargs["body"]["table"], dict):  
                    process_id = kwargs["body"]['table']['process_id']
                else:
                    table = kwargs["body"]['table']
            elif "register" in kwargs["body"]:
                process_id =  kwargs["body"]['register']['process_id']
            elif "process_id" in kwargs["body"]:
                process_id =  kwargs["body"]["process_id"]
                if "user_id" in kwargs["body"]:
                    user_id = kwargs["body"]["user_id"]
            else:
                process_id = None
        else:
            process_id = None
    else:
        process_id = None
    # split the process_id from the end of the route 
    if process_id is not None:
        # TODO: remove only the last one, currently removes any /<process_id> from the route
        route = route.replace('/'+str(process_id), '')
    # set tables if the get_params or the body_params contain a "table" key
    print("process_id = ", process_id)
    print("route = ", route)
    if route == "/logs": 
        table = "log"
    elif route == "/authorizations": 
        table = "authorization"
    elif route == "/users": 
        table = "user"
    elif body_params is not None:
        if "table" in body_params:
            if isinstance(body_params['table'], str):
                table = body_params['table']
            else:
                table = body_params['table']['name']
        elif "table" in get_params:
            table = get_params['table']
        else: 
            table = None
    else:
        table = None
    # perform a query to the authorizations table
    if table is None:
        rules = Authorization.query.filter_by(user_id = current_user.id, process_id = process_id, table = None ).order_by(Authorization.priority.asc()).all()
    else:
        rules = Authorization.query.filter_by(user_id = current_user.id, process_id = process_id, table = table).order_by(Authorization.priority.asc()).all()
    # grants permissions to admin
    if current_user.admin:
        auth = True
    else:
        # set the auth default value to false
        auth = False
        # if there is no table set, verify if process_crud is true
        if table is None:
            for r in rules:
                # process_crud permission
                if r.process_crud: auth = True    
        else:
            for r in rules:
                # table_crud permission
                if r.table_crud: auth = True
            # if table_crud was false, check other authorization fields
            if auth == False:
                # check each of the authorization fields that are True and set auth to True only if all conditions are met
                for r in rules:
                    # create permission
                    if method == 'POST' and process_id is None and r.create: auth = True
                    # read permission
                    if method == 'GET' and process_id is not None and r.read: auth = True
                    # read_all permission
                    if method == 'GET' and process_id is None and r.read_all: auth = True
                    # update permission
                    if method == 'PUT' and process_id is not None and r.update: auth = True
                    # delete permission
                    if method == 'DEL' and process_id is not None and r.delete: auth = True
    return auth

