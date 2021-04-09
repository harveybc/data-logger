""" Map this model's fields and relationships """

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.base.util import hash_pass
from app.db_init import db
from app.app import login_manager
from sqlalchemy.orm import relationship
import json

class User(db.Model, UserMixin):
    """ Map the user table columns and bidirectional one-to many relationship with process """
    __tablename__ = 'user'
    
    # columns
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    admin = Column(Boolean)
    password = Column(String)

    # realationships
    processes = relationship("Process", back_populates='user')


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

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

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
