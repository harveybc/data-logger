""" Controller for the authorization endpoints. 
    Description: Contains API endpoint handler functions for CRUD operations 
    on the authorizations table whose registers are an ordered set of rules
    that a request must approve to perform its intended action.
    
    By default, admin users can CRUD processes, tables and table registers.
    
    Also by default, all users can read/create registers on their processes' tables, 
    but can't create processes or tables, and can't update/delete registers.

    When authorizations are created for an user, process or a table
    the user is denied all access but the indicated.

    The list of authorizations for an user, proess or table is ordered by the 
    priority column in ascending order and the highest priority rules override 
    the lowest priority ones.

"""

def create():
    """ Parse command line parameters.

        Args:
        args ([str]): command line parameters as list of strings

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """
    #return 'You created the user id='+id+', username='+username+', email='+email+', password='+password+', is_admin='+is_admin 

def read():
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

def read_all():
    """ Parse command line parameters.

        Args:
        args ([str]): command line parameters as list of strings

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """






