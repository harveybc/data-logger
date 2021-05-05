""" Controller for the user endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""

from models.user import User
from app.app import db
import json
from sqlalchemy.exc import SQLAlchemyError

def create(body): 
    """ Create a register in db based on a json from a request's body parameter.

        Args:
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created user register with empty password field.
    """
    # instantiate user with the body dict as kwargs
    new_user = User(**body)
    # create new flask-sqlalchemy session
    db.session.add(new_user)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # test if the new user was created 
    try:
        res = User.query.filter_by(username=new_user.username).first_or_404()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # empty pass
    res.password=""
    # return register as dict
    return res.as_dict()

def read(userId):
    """ Query a register in db based on the id field of the user model, obtained from a request's userId url parameter.

        Args:
        userId (str): id field of the user model, obtained from a request's userId url parameter (users/<userId>).

        Returns:
        res (dict): the requested user register with empty password field.
    """ 
    try:
        res = User.query.filter_by(id=userId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # empty pass
    res.password=""
    return res.as_dict()
    

def update(userId, body):
    """ Update a register in db based on a json from a request's body parameter.

        Args:
        userId (str): id field of the user model, obtained from a request's userId url parameter (users/<userId>).
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created user register with empty password field.
    """
    # query the existing register
    try:
        res = User.query.filter_by(id=userId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # replace model with body fields
    body['id']=res.id
    res.__dict__ = body
    # perform update 
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # test if the model was updated 
    try:
        res2 = User.query.filter_by(id=int(userId)).first_or_404()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # empty pass
    res2.password=""
    # return register as dict
    return res2.as_dict()

def delete(userId):
    """ Delete a register in db based on the id field of the user model, obtained from a request's userId url parameter.

        Args:
        userId (str): id field of the user model, obtained from a request's userId url parameter (users/<userId>).

        Returns:
        res (int): the deleted register id field
    """ 
    try:
        res = User.query.filter_by(id=userId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # perform delete 
    db.session.delete(res)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    return res.id

def read_all():
    """ Query all registers of the user model.

        Returns:
        res (dict): the requested user registers with empty password field.
    """ 
    try:
        res = User.query.all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # convert to list of dicts and empty pass
    res2 =[]
    for r in res:
        r.password = ""
        res2.append(r.as_dict())
    return res2
   




