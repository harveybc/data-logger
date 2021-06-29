""" Common Controller Functions 
    Description: Contains functions used by most controllers
"""
from functools import wraps
from flask import (current_app)

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


def is_authorized():
    #TODO: Verify if the function requires parameters or the request parameters can be obtained from this function (First Option)
    """ Verify if a request is authorized for the current user.
        
        Returns:
        res (dict): true if the user is authorized for the request 
    """ 
    method = route = route_params = get_params = body_params = None    return False

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