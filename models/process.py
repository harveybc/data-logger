""" Map this model's fields and relationships """
    
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.base.util import hash_pass
from app.app import db
from app.app import login_manager
import datetime
from sqlalchemy.orm import relationship

class Process(db.Model):
    """ Map the process table columns and bidirectional one-to-many relationship with user """
    __tablename__ = 'process'

    # columns
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    tables=Column(String)
    created=Column(DateTime, default=datetime.datetime.utcnow)
    user_id=Column(Integer, ForeignKey('user.id'))

    # relationships
    user = relationship("User", back_populates='processes')


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str) and not isinstance(value, dict):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                print("value=", value)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)

    def as_dict(self):   
        r2 = {}
        for c in self.__table__.columns:
            attr = getattr(self, c.name)
            if is_num(attr):
                r2[c.name]=attr
            else:
                r2[c.name]=str(attr)
        return r2



