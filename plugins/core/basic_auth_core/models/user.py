""" Model for the user table. 
    Description: Contains the model's class, atributes, initialization and representation.
"""

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from .authorization import Authorization
from app.app import db

# TODO: Activate cache for the user table select queries in database since they are made in every other request
# TODO: use indexes in all searchable non numeric columns.
class User(db.Model, UserMixin, BaseModel):
    """ Map the user table columns and bidirectional one-to many relationship with process """
    __tablename__ = 'user'
    
    # columns
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    admin = Column(Boolean)
    password = Column(String)

    # relationships
    #children = relationship("Child", backref="parent")
    processes = relationship("Process", backref='process_user')
    authorizations = relationship("Authorization", backref='authorization_user')    
    logs = relationship("Log", backref='log_user')

    # representation
    def __repr__(self):
        return str(self.username)



