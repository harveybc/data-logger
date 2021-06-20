""" Map this model's fields and relationships """

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

# TODO: activate cache for read authorization table select queries, since they are made in every other request
# TODO: use indexes in all searchable non numeric columns.
class Authorization(db.Model, BaseModel):
    """ Map the process table columns and bidirectional one-to-many relationship with user """
    __tablename__ = 'process'

    # columns
    id = Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey('user.id'))
    process_id=Column(Integer, ForeignKey('process.id'))
    name = Column(String, unique=True)
    table=Column(String)
    created=Column(String, default=str(datetime.now()))
    description = Column(String)
    
    # relationships
    user = relationship("User", back_populates='processes')

    def __repr__(self):
        return str(self.name)
