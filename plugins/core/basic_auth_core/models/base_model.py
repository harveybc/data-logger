""" Base Model. 
    Description: Contains common methods for all models.
""" 
import datetime
from app.util import hash_pass
from app.app import login_manager
import base64

class BaseModel():
       
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if isinstance(value, list) or isinstance(value, tuple):
                if len(value) == 1:
                    if  not isinstance(value, str) and not isinstance(value, dict):
                        value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def as_dict(self):   
        r2 = {}
        for c in self.__table__.columns:
            attr = getattr(self, c.name)
            if is_num(attr):
                r2[c.name]=attr
            else:
                r2[c.name]=str(attr)
        return r2
        
def is_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False

from .user import User

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def load_user_from_request(request):

    # try to login using Basic Auth
    credentials = request.headers.get('Authorization')
    if credentials:
        credentials = credentials.replace('Basic ', '', 1)
        try:
            credentials = base64.b64decode(credentials)
        except TypeError:
            pass
        cred_list = credentials.decode().split(':')
        username = cred_list[0]
        password = cred_list[1]
        user = User.query.filter_by(username=username).first()
        if user:
            return user

    # finally, return None if did not login the user
    return None