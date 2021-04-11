""" Controller for the user endpoint. 
    Description: Contains API endpoint handler functions for CRUD operations.  
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
        new_user (dict): the newly created user register with empty password field.
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
    
def get(userId):
    """ Parse command line parameters.
                  
        Args:
        args ([str]): command line parpameters as list of strings

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """
    res = User.query.filter_by(id=int(userId)).first_or_404()
    return res.as_dict()
    

def update():
    """ Parse command line parameters.

        Args:
        args ([str]): command line parameters as list of strings

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """

def delete():
    """ Parse command line parameters.

        Args:
        args ([str]): command line parameters as list of strings

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """

def get_list():
    """ Parse command line parameters.

        Args:
        args ([str]): command line parameters as list of strings

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """
    res = User.query.all()
    r2 =[]
    for r in res:
        r2.append(r.as_dict())
    return r2
   




