""" Map this model's fields and relationships """

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from .base_model import BaseModel

class Process(db.Model, BaseModel):
    """ Map the process table columns and bidirectional one-to-many relationship with user """
    __tablename__ = 'process'

    # columns
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String, default="")
    tables=Column(String, server_default="[]")
    created=Column(String, default=str(datetime.now()))
    user_id=Column(Integer, ForeignKey('user.id'), default=0)

    # relationships
    users = relationship("User", back_populates='processes')
    authorizations = relationship("Authorization", back_populates='processes')
    logs = relationship("Log", back_populates='processes')

    def __repr__(self):
        return str(self.name)
