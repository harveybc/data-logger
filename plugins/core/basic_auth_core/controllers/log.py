""" Controller for the log endpoints. 
    Description: Contains API endpoint handler functions for CRUD operations 
    on the log table whose registers are an historic set of registers
    containing the requests made to the server and the results of those requests.
"""

from app.app import db
import json
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from datetime import datetime
from app.app import login_manager
from ..models.log import Log
from ..models.process_table import ProcessTable
from ..models.process_register_factory import ProcessRegisterFactory
from sqlalchemy.ext.automap import automap_base
from ..controllers.common import as_dict, is_num
from flask import request
from functools import wraps

def log_required(func):
    """ This decoration indicates that a new log has to be created before executing the decorated function.

        Args:
        func (function): The function to be decorated

        Returns:
        res (dict): func if the user is authorized, login_manager.unauthorized() 
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # perform  request logging before actually calling the function
        log_request(*args, **kwargs)
        return func(*args, **kwargs)
    return decorated_view

from ..controllers.authorization import authorization_required

@authorization_required
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
        db.session.expunge_all()
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
    return as_dict(res)

@authorization_required
def read(log_id):
    """ Performs a query log register.

        Args:
        process_id (str): log_id (log/<log_id>).

        Returns:
        res (dict): the requested  register.
    """
    try:
        res = as_dict(Log.query.filter_by(id=log_id).one())
    except SQLAlchemyError as e:
        error = str(e)
        return error 
    return res

@authorization_required
@log_required
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
        db.session.expunge_all()
                db.session.close()
    except SQLAlchemyError as e:
        error = str(e)
        res = { 'error_b' : error}
    # test if the model was updated 
    try:
        res = as_dict(Log.query.filter_by(id=int(log_id)).one())
        db.session.expunge_all()
                db.session.close()
    except SQLAlchemyError as e:
        error = str(e)
        res = { 'error_c' : error}
    return res

@authorization_required
@log_required
def delete(log_id):
    """ Delete a register in db based on the id field of the authorizarions model, obtained from a request's log_id url parameter.

        Args:
        process_id (str): id field , obtained from a request's url parameter (log/<log_id>).

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

@authorization_required
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
        res2.append(as_dict(r))
    return res2

def log_request(*args, **kwargs):
    """ Log the current request.
        
        Args:
        process_id (int): The id of the process of the request to be logged (may be None)

        Returns:
        res (dict): the id in the log table of the new log register, -1 if error
    """ 
    log_params = {}
    log_params['method'] = request.method
    
    log_params['route'] = request.path
    log_params['parameters'] = json.dumps(request.args)
    log_params['body'] = json.dumps(request.json)
    log_params['process_id'] = None
    log_params['user_id'] = current_user.id
    # find process_id from args
    # if args[0] is None(read_all controller), process_id = request.args.get("process_id")
    if len(kwargs) > 0:
        if "process_id" in kwargs:
            log_params['process_id'] = kwargs["process_id"]
        # if args[0] is a dict (update controller), if table is in args[0], process_id = args[0]['table']['process_id'], else process_id =  args[0]['register']['process_id']
        elif "body" in kwargs:
            if "user_id" in kwargs["body"]:
                   log_params['user_id'] = kwargs["body"]["user_id"]
            if "table" in kwargs["body"]:
                if isinstance(kwargs["body"]["table"], dict):  
                    log_params['process_id'] = kwargs["body"]['table']['process_id']
                else:
                    log_params['table'] = kwargs["body"]['table']
            elif "register" in kwargs["body"]:
                log_params['process_id'] =  kwargs["body"]['register']['process_id']
            elif "process_id" in kwargs["body"]:
                log_params['process_id'] =  kwargs["body"]["process_id"]
                
            else:
                log_params['process_id'] = None
        else:
            log_params['process_id'] = None
    else:
        log_params['process_id'] = None
    # split the process_id from the end of the route 
    if log_params['process_id'] is not None:
        # TODO: remove only the last one, currently removes any /<process_id> from the route
        log_params['route'] = log_params['route'].replace('/'+str(log_params['process_id']), '')
    # set tables if the get_params or the body_params contain a "table" key
    if log_params['route'] == "/logs": 
        log_params['table'] = "log"
    elif log_params['route'] == "/authorizations": 
        log_params['table'] = "authorization"
    elif log_params['route'] == "/users": 
        log_params['table'] = "user"
    elif request.json is not None:
        body_params = request.json 
        if "table" in body_params:
            if isinstance(body_params['table'], str):
                log_params['table'] = body_params['table']
            else:
                log_params['table'] = body_params['table']['name']
        elif "table" in request.args:
            log_params['table'] = request.args['table']
        else: 
            log_params['table'] = None
    else:
        log_params['table'] = None
    # create a new log table register
    new_log = Log(**log_params)
    # add the new_log to the session
    db.session.add(new_log)
    try:
        db.session.commit()
        new_id = new_log.id
        #db.session.expunge_all()
                db.session.close()
    except SQLAlchemyError as e:
        error = str(e)
        return -1
    return new_id

def result_log_required(id, code, result):
    """ This function updates a request log with the result of the request before the function returns.

        Args:
        id (integer): The id field of the log register to be updated
        code (integer): HTTP result code
        result (string): The result of the result of the request to be updated on the log

        Returns:
        res (dict): True if the log was updated, False on error
    """
    # query the existing register
    try:
        log_model = Log.query.filter_by(id=id).one()
    except SQLAlchemyError as e:
        error = str(e)
        return False
    # replace code and result on the model 
    setattr(log_model, 'code', code)
    setattr(log_model, 'result', result)
    # perform update 
    try:
        db.session.commit()
        db.session.expunge_all()
                db.session.close()
    except SQLAlchemyError as e:
        error = str(e)
        return False
    return True







