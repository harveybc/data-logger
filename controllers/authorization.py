""" Controller for the authorization endpoints. 
    Description: Contains API endpoint handler functions for CRUD operations 
    on the authorizations table whose registers are an ordered set of rules
    that a request must approve to perform its intended action.
    
    By default, admin users can CRUD processes, tables and table registers.
    
    Also by default, all users can read/create registers on their processes' tables, 
    but can't create processes or tables, and can't update/delete registers.

    When authorizations are created for an user, process or a table
    the user, process or table is denied all access but the indicated.

    The list of authorizations for an user, process or table is ordered by the 
    priority column and the highest priority rules override the lowest priority ones.

"""

from app.app import db
import json
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from datetime import datetime
from app.app import login_manager
from models.authorization import Authorization
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

def read(authorization_id):
    """ Performs a query authorization register.

        Args:
        processId (str): authorization_id (authorization/<authorization_id>).

        Returns:
        res (dict): the requested  register.
    """
    try:
        res = Authorization.query.filter_by(id=authorization_id).one().as_dict()
    except SQLAlchemyError as e:
        error = str(e)
        return error 
    return res

def update():
    """ Parse command line parameters.

        Args:
        args ([str]): command line parameters as list of strings

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """

def delete(authorization_id):
    """ Parse command line parameters.

        Args:
        args ([str]): command line parameters as list of strings

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
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

@login_required
def read_all():
    """ Query all registers of the authorizations table.

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






