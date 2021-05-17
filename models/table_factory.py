""" Map this model's fields and relationships """

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from pydoc import locate 

class ProcessTable(db.Model, BaseModel):
    """ Map the table columns  """
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
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

        # TODO: relationships
        #user = relationship("User", back_populates='processes')

    def __repr__(self):
        return str(self.name)

class TableFactory:
    
    def __init__(self, **kwargs):
        self.new_table =  ProcessTable(kwargs)
    
    def factory(self):
        return(self.new_table)

