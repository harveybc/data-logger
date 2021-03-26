""" Performs Basic Authentication """

import connexion
from connexion.decorators.security import validate_scope
from connexion.exceptions import OAuthScopeProblem
# the user model is used for authentication
from models.user import User


def authenticate(username, password, required_scopes=None):
    """ Performs basic authentication from the user table in the database
                  
        Args:
        username (str): username
        password (str): password

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """
    # query for the username and pass for the username



    # compare the db pass with the request one

    if username == 'test0' and password == 'test0':
        info = {'sub': 'test0', 'scope': 'secret'}
    elif username == 'foo' and password == 'bar':
        info = {'sub': 'user1', 'scope': ''}
    else:
        # optional: raise exception for custom error response
        return None

    # optional
    if required_scopes is not None and not validate_scope(required_scopes, info['scope']):
        raise OAuthScopeProblem(
                description='Provided user doesn\'t have the required access rights',
                required_scopes=required_scopes,
                token_scopes=info['scope']
            )

    return info
