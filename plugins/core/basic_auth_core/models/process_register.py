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
from ..controllers.common import as_dict, is_num
from app.util import sanitize_str

def ProcessRegister(table_param):
    # Process register model factory
    class NewModel(db.Model):    
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
            table_param = sanitize_str(register['table'], 256)
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

        def read(self, process_id, table_param, reg_id):
            """ Performs a query to a process table register.

                Args:
                process_id (str): id field of the process model.

                table_param (str): name of the table 

                Returns:
                res (model): the requested process table.
            """ 
            register_model = eval("Base.classes." + table_param)
            # perform query
            reg_id = sanitize_str(reg_id)
            res=db.session.query(register_model).filter_by(id=reg_id).one()
            return res
        
        def read_all(self, process_id, table_param):
            """ Query all registers of the process table register.
                
                Args:
                process_id (str): id field of the process model.

                table_param (str): name of the table 
                
                Returns:
                res (list): the requested list of registers.
            """ 
            # generate list of registers
            # TODO: filter by column,value
            # TODO: validate if the table is in the process tables array
            table_param = sanitize_str(table_param, 256)
            register_model = eval("Base.classes." + table_param)
            # perform query
            res=db.session.query(register_model).all()
            return [as_dict(c) for c in res]


        def update(self, register):
            """ Update a register in db based on a json from a request's body parameter.

                Args:
                register (dict): dict containing the register values
                table_param (dict): name of the table

                Returns:
                register_model (model): the updated model
            """
            table_param = sanitize_str(register['table'])
            register_model = eval("Base.classes." + table_param)
            # perform query
            model = db.session.query(register_model).filter_by(id=register['reg_id']).one()
            # set the new values from the values array
            for property, value in register['values'].items():
                setattr(model, property, value)
            # update the register
            try:
                db.session.commit()
                db.session.close()
            except SQLAlchemyError as e:
                error = str(e)
                res['register'] ={ 'error_d' : error}
            return register_model

        def delete(self, process_id, table_param, reg_id):
            """ Delete a register in db based on the id field of the process model, obtained from a request's process_id url parameter.

                Args:
                process_id (str): id field of the process model, obtained from a request's process_id url parameter (processs/<process_id>).

                Returns:
                res (int): the deleted register id field
            """  
            # sanitize the input string and limit its length
            table_param = sanitize_str(table_param, 256)
            register_model = eval("Base.classes." + table_param)
            try:
                res=db.session.query(register_model).filter_by(id=reg_id).one()
            except SQLAlchemyError as e:
                error = str(e)
                return error
            # perform register delete 
            db.session.delete(res)
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                error = str(e)
                return error
            return reg_id
    NewModel.__name__ = table_param
    return NewModel