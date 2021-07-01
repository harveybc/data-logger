""" Common Controller Functions 
    Description: Contains functions used by most controllers
"""
from functools import wraps
from flask import (current_app)
from flask import request
from string import split
from models.authorization import Authorization
from flask_login import current_user

def as_dict(model):   
    """ Transform a sqlalchemy result into a dict
        Args:
        model (sqlalachemy result): the result of a sqlalachemy query for an individual register.

        Returns:
        res (dict): the model transformed into a dict.
    """ 
    r2 = {}
    for c in model.__table__.columns:
        attr = getattr(model, c.name)
        if is_num(attr):
            r2[c.name]=attr
        else:
            r2[c.name]=str(attr)
    return r2

def is_num(n):
    """ Verify if an input variable is int or float.

        Args:
        n (variable): The variable to be verified as number

        Returns:
        res (dict): true if the variable is a float or int, false otherwise
    """ 
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False


def is_authorized(process_id):
    """ Verify if a request is authorized for the current user.
        
        Args:
        n (variable): The variable to be verified as number

        Returns:
        res (dict): true if the user is authorized for the request 
    """ 
    method = request.method
    route = request.path
    get_params = request.args
    body_params = request.json
    # split the process_id from the end of the route 
    if process_id is not None:
        # TODO: remove only the last one, currently removes any /<process_id> from the route
        route = route.replace('/'+str(process_id), '')
    # set tables if the get_params or the body_params contain a "table" key
    if "table" in body_params:
        table = body_params.table.name
    elif "table" in get_params:
        table = get_params.table
    else: 
        table = None
    # perform a query to the authorizations table
    if table is None:
        Authorization.query.filter_by(user_id = current_user.id, process_id = process_id ).all()
    else:
        Authorization.query.filter_by(user_id = current_user.id, process_id = process_id, table = table).all()
    
    # set the auth default value to false
    auth = False
    # check each of the autorization fields that are True and set auth to True only if all conditions are met

    
    return False

def log_request():
    #TODO: Verify if the function requires parameters or the request parameters can be obtained from this function (First Option)
    """ Create a register in the log table.

        Returns:
        res (dict): true if the request was succesfully loaded. 
    """ 
    method = route = route_params = get_params = body_params = None
    return True
    
def authorization_required(func):
    """ This decoration indicates that the decorated function should verify if the current user is authorized for the current request.

        Args:
        func (function): The function to be decorated

        Returns:
        res (dict): func if the user is authorized, login_manager.unauthorized() 
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if is_authorized():
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()
    return decorated_view

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
        log_request()
        return func(*args, **kwargs)
    return decorated_view

def result_log_required(id, val):
    """ This function updates a request log with the result of the request before the function returns.

        Args:
        id (integer): The id field of the log register to be updated
        val (string): The result of the result to be updated

        Returns:
        res (dict): func if the user is authorized, login_manager.unauthorized() 
    """
    pass