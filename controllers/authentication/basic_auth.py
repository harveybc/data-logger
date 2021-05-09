""" Performs Basic Authentication """

import connexion
from connexion.decorators.security import validate_scope
from connexion.exceptions import OAuthScopeProblem
# the user model is used for authentication
from models.user import User
from app.app import db
from app.base.util import verify_pass_str

def authenticate(username, password, required_scopes=None):
    """ Performs basic authentication from the user table in the database
                  
        Args:
        username (str): username
        password (str): password

        Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """

    # perform query
    user_model = User.query.filter_by(username=username).first()

    # compare the db pass with the request one
    if verify_pass_str(password, user_model.password) and user_model.admin == True:
        info = {'sub': username, 'scope': 'admin'}
    elif password == user_model.password:
        info = {'sub': username, 'scope': ''}
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
