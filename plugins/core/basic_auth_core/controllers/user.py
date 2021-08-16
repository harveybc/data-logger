""" Controller for the user endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""

from ..models.user import User
from app.app import db
import json
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.attributes import flag_dirty, flag_modified
from ..controllers.authorization import authorization_required
from ..controllers.log import log_required
from app.util import as_dict

@authorization_required
@log_required
def create(body): 
    """ Create a register in db based on a json from a request's body parameter.

        Args:
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created user register with empty password field.
    """
    # instantiate user with the body dict as kwargs
    new_user = User.create(body)
    # test if the new user was created 
    try:
        res = User.query.filter_by(username=new_user.username).first_or_404()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # empty pass
    res2 = as_dict(res)
    res2["password"] =""
    # return register as dict
    return res2

@authorization_required
@log_required
def read(userId):
    """ Query a register in db based on the id field of the user model, obtained from a request's userId url parameter.

        Args:
        userId (str): id field of the user model, obtained from a request's userId url parameter (users/<userId>).

        Returns:
        res (dict): the requested user register with empty password field.
    """ 
    res = User.read(userId)
    # empty pass
    res2 = as_dict(res)
    res2["password"]=""
    return res2
    
@authorization_required
@log_required
def update(body, userId):
    """ Update a register in db based on a json from a request's body parameter.

        Args:
        userId (str): id field of the user model, obtained from a request's userId url parameter (users/<userId>).
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created user register with empty password field.
    """
    # update the existing register
    res = User.update(body, userId)
    # empty pass
    res2 = as_dict(res)
    res2["password"]=""
    # return register as dict
    return res2

@authorization_required
@log_required
def delete(userId):
    """ Delete a register in db based on the id field of the user model, obtained from a request's userId url parameter.

        Args:
        userId (str): id field of the user model, obtained from a request's userId url parameter (users/<userId>).

        Returns:
        res (int): the deleted register id field
    """ 
    res = User.delete(userId)
    return res

@authorization_required
@log_required
def read_all():
    """ Query all registers of the user model.

        Returns:
        res (dict): the requested user registers with empty password field.
    """ 
    res = User.read_all()
    res2 =[]
    for r in res:
        r2 = as_dict(r)
        r2["password"] = ""
        res2.append(r2)
    return res2

   




