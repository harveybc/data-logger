""" Map this model's fields and relationships """

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

# TODO: activate cache for read authorization table select queries, since they are made in every other request
# TODO: use indexes in all searchable non numeric columns.
class Log(db.Model, BaseModel):
    """ Map the process table columns and bidirectional one-to-many relationship with user """
    __tablename__ = 'log'

    # columns
    id = Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey('user.id'))
    process_id=Column(Integer, ForeignKey('process.id'))
    table=Column(String)
    route = Column(String)
    method = Column(String)
    parameters = Column(String)
    body = Column(String)
    result_code = Column(Integer)
    result = Column(String)
    
    
    # relationships
    users = relationship("User", back_populates='authorizations')
    processes = relationship("Process", back_populates='authorizations')

    def __repr__(self):
        return str(self.name)
