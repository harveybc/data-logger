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

def get():
    """ Parse command line parameters.
                  
        Args:
        args ([str]): command line parameters as list of strings

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """
    return 'id='+id+', username='+username+', email='+email+', password='+password+', is_admin='+is_admin 

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

    return json.dumps(res)
   




