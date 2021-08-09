""" Create the statements required by the process controller for CRUD in a table from a process """

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, MetaData, Table, insert, update
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from pydoc import locate 
from copy import deepcopy
from sqlalchemy.ext.automap import automap_base
from ..models.process import Process
import json
from sqlalchemy.exc import SQLAlchemyError

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

    def create(self, register): 
        """ Create a register in a process' table
        
            Args:
            register (dict): dict containing the fields of the new register, obtained from json in the body of the request.

            Returns:
            res (dict): the newly created register model
        """  
        # sanitize the input string and limit its length
        table_param = self.sanitize_str(register['table'], 256)
        register_base = eval("self.Base.classes." + table_param)
        # set the new values from the values array
        register_model = register_base(**register['values'])
        # update the register
        try:
            db.session.add(register_model)
            db.session.commit()
            new_id = register_model.id
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res ={ 'error_d' : error}
        return res

