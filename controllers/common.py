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
    """ Verify if a request is authorized for the current user.
    |
        Returns:
        res (dict): true if the user is authorized for the request 
    """ 
    
    return True

def log_request():
    """ Create a register in the log table.
        TODO: Verify if the function requires parameters or the request parameters can be obtained from this function (First Option)
        Returns:
        res (dict): true if the request was succesfully loaded. 
    """ 
    pass
    
def authorization_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if is_authorized():
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()
    return decorated_view

def log_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # perform  request logging before actually calling the function
        log_request()
        return func(*args, **kwargs)
    return decorated_view