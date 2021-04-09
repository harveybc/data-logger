""" Handlers for the user endpoint  """

from models.user import User
from app.app import db
import json

def create():
    """ Parse command line parameters.

        Args:
        args ([str]): command line parameters as list of strings

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """
    #return 'You created the user id='+id+', username='+username+', email='+email+', password='+password+', is_admin='+is_admin 

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
   




