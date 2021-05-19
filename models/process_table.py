""" Map this model's fields and relationships """

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, MetaData
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from pydoc import locate 

class ProcessTable():
    """ Map the table columns  """
    def __init__(self, **kwargs):
        # extract kwargs into class attributes
        for property, value in kwargs.items():
            setattr(self, property, value)
        # initialize Table class parameters list
        t_args = []
        # add the name
        t_args.append(self.name)
        # add metadata
        t_args.append(MetaData())
        # add columns 
        for c in self.columns:
            if c.primary_key:
                t_args.append(Column(c.name, locate(c.col_type), primary_key=c.primary_key))
            elif c.foreign_key == "none":
                t_args.append(Column(c.name, locate(c.col_type), ForeignKey(c.foreign_key), unique=c.unique, index=c.index, default=c.default, nullable=c.nullable))
            else:
                t_args.append(Column(c.name, locate(c.col_type), unique=c.unique, index=c.index, default=c.default, nullable=c.nullable))
        # TODO: relationships
        #user = relationship("User", back_populates='processes')
    def __repr__(self):
        return str(self.name)
    

    def factory(self, **kwargs):
        self.new_table =  self.Process(kwargs)
        return(self.new_table)

