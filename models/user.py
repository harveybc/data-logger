""" Model for the user table. 
    Description: Contains the model's class, atributes, initialization and representation.
"""

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from flask_login import LoginManager
from app.app import login_manager
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class User(BaseModel, UserMixin):
    """ Map the user table columns and bidirectional one-to many relationship with process """
    __tablename__ = 'user'
    
    # columns
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    admin = Column(Boolean)
    password = Column(String)

    # relationships
    processes = relationship("Process", back_populates='user')

    # representation
    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
