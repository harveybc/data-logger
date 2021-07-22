""" Create the statements required by the process controller for CRUD in a table from a process """

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, MetaData, Table, insert, update
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from pydoc import locate 

class ProcessRegister():
    """ Map the columns to a list of register constructor arguments  adn create a statement to be executed by the controller"""
    def __init__(self, **kwargs):
        # extract kwargs into class attributes
        for property, value in kwargs.items():
            setattr(self, property, value)
        # set the table
        self.meta_table = db.metadata.tables[self.table]
        #print(db.metadata.tables)

    def create_stmt(self):
        return insert(self.meta_table).values(self.values)

    def update_stmt(self):
        return update(self.meta_table).where(self.meta_table.c.id == self.reg_id).values(self.values)

    def __repr__(self):
        return str(self.table)

    