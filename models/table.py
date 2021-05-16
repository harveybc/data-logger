""" Map this model's fields and relationships """

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from pydoc import locate 

class Table(db.Model, BaseModel):
    """ Map the table columns and bidirectional one-to-many relationship with user """
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if isinstance(value, list) or isinstance(value, tuple):
                if len(value) == 1:
                    if  not isinstance(value, str) and not isinstance(value, dict):
                        value = value[0]
            setattr(self, property, value)
    
        # table name
        self.__tablename__ = self.name
        
        # set each column name, indexes and types from this list:
        # https://docs.sqlalchemy.org/en/14/core/type_basics.html#generic-types 
        for c in self.columns:
            if c.primary_key:
                setattr(self, c.name, Column(locate(c.col_type), primary_key=c.primary_key))
            elif c.foreign_key == "none":
                setattr(self, c.name, Column(locate(c.col_type), ForeignKey(c.foreign_key), unique=c.unique, index=c.index), default=c.default)
            else:
                setattr(self, c.name, Column(locate(c.col_type), unique=c.unique, index=c.index, default=c.default))
        id = Column(Integer, primary_key=True)
        process_id = Column(String, unique=True, index=True)
        description = Column(String)
        tables=Column(String)
        created=Column(String, default=str(datetime.now()))
        user_id=Column(Integer, ForeignKey('user.id'))

        # relationships
        #user = relationship("User", back_populates='processes')

    def __repr__(self):
        return str(self.name)
