""" Map this model's fields and relationships """

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from .base_model import BaseModel

# TODO: activate cache for read authorization table select queries, since they are made in every other request
# TODO: use indexes in all searchable non numeric columns.
class Authorization(db.Model, BaseModel):
    """ Map the process table columns and bidirectional one-to-many relationship with user """
    __tablename__ = 'authorization'

    # columns
    id = Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey('user.id'))
    process_id=Column(Integer, ForeignKey('process.id'))
    table=Column(String)
    read_all = Column(Boolean)
    read = Column(Boolean)
    create = Column(Boolean)
    update = Column(Boolean)
    delete = Column(Boolean)
    table_crud = Column(Boolean)
    process_crud = Column(Boolean)
    priority=Column(Integer, default=0)
    created=Column(String, default=str(datetime.now()))
    
    # relationships
    users = relationship("User", back_populates='authorizations')
    processes = relationship("Process", back_populates='authorizations')

    def __repr__(self):
        return str(self.name)
