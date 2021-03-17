""" Performs Basic Authentication """

import connexion
from connexion.decorators.security import validate_scope
from connexion.exceptions import OAuthScopeProblem


def basic_auth(username, password, required_scopes=None):
    """ Performs basic authentication from the user table in the database
                  
        Args:
        username (str): username
        password (str): password

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """
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
