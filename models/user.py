""" Model for the user table. 
    Description: Contains the model's class, atributes, initialization and representation.
"""

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from app.app import db

# TODO: Activate cache for the user table select queries in database since they are made in every other request
# TODO: use indexes in all searchable non numeric columns.
class User(db.Model, BaseModel, UserMixin):
    """ Map the user table columns and bidirectional one-to many relationship with process """
    __tablename__ = 'user'
    
    # columns
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    admin = Column(Boolean)
    password = Column(String)

    # relationships
    processes = relationship("Process", back_populates='users')
    authorizations = relationship("Authorization", back_populates='users')    
    #logs = relationship("Log", back_populates='users')

    # representation
    def __repr__(self):
        return str(self.username)



