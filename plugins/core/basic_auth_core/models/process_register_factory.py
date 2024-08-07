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
from app.util import sanitize_str, reflect_prepare

def ProcessRegisterFactory(table_param, BaseAutoMap):
    
    # Process register model factory
    class NewModel():    
        """ Map the columns to a list of register constructor arguments  adn create a statement to be executed by the controller"""
        table_name = sanitize_str(table_param, 256)
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True} 
        id = Column(Integer, primary_key=True)
        Base = BaseAutoMap
        
        
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
        
        @classmethod
        def create(cls, **register): 
            """ Create a register in a process' table
            
                Args:
                register (dict): dict containing the fields of the new register, obtained from json in the body of the request.

                Returns:
                res (dict): the newly created register model
            """  
            # sanitize the input string and limit its length
            table_name = sanitize_str(register['table'], 256)
            Base.prepare(db.engine, reflect=False)
            #register_base = Base.classes.test_table
            register_base = eval("Base.classes." + table_name)
            # set the new values from the values array
            register_model = register_base(**register['values'])
            # update the register
            try:
                db.session.add(register_model)
                db.session.commit()
                new_id = register_model.id
                ##db.session.expunge_all()
                ##db.session.close()
                res = as_dict(register_model)
            except SQLAlchemyError as e:
                error = str(e)
                print("Error : " , error)
                res ={ 'error_c' : error}
            return res
        
        @classmethod
        def read(cls, reg_id):
            """ Performs a query to a process table register.

                Args:
                process_id (str): id field of the process model.

                table_param (str): name of the table 

                Returns:
                res (model): the requested process table.
            """ 
            table_param = sanitize_str(table_param, 256)
            register_model = eval("Base.classes." + table_param)
            # perform query
            res=db.session.query(register_model).filter_by(id=reg_id).one()
            return res
        
        @classmethod
        def read_all(cls, process_id, table_param, BaseParam):
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
            Base = BaseParam
            table_name = sanitize_str(table_param, 256)
            register_model = eval("Base.classes." + table_name)
            # perform query
            res=db.session.query(register_model).all()
            return [as_dict(c) for c in res]

        @classmethod
        def update(cls, **register):
            """ Update a register in db based on a json from a request's body parameter.

                Args:
                register (dict): dict containing the register values
                table_param (dict): name of the table

                Returns:
                register_model (model): the updated model
            """
            table_name = sanitize_str(table_param, 256)
            Base.prepare(db.engine, reflect=True)
            register_model = eval("Base.classes." + table_name)
            # perform query
            model = db.session.query(register_model).filter_by(id=register['id']).one()
            # set the new values from the values array
            for property, value in register['values'].items():
                setattr(model, property, value)
            # update the register
            try:
                db.session.commit()
                ##db.session.expunge_all()
                ##db.session.close()
            except SQLAlchemyError as e:
                error = str(e)
                print("Error : " , error)
                res['register'] ={ 'error_e' : error}
            return as_dict(model)

        @classmethod
        def delete(cls, reg_id):
            """ Delete a register in db based on the id field of the process model, obtained from a request's process_id url parameter.

                Args:
                process_id (str): id field of the process model, obtained from a request's process_id url parameter (processs/<process_id>).

                Returns:
                res (int): the deleted register id field
            """  
            # sanitize the input string and limit its length
            table_name = sanitize_str(table_param, 256)
            register_model = eval("Base.classes." + table_name)
            try:
                res=db.session.query(register_model).filter_by(id=reg_id).one()
            except SQLAlchemyError as e:
                error = str(e)
                print("Error : " , error)
                return error
            # perform register delete 
            db.session.delete(res)
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                error = str(e)
                print("Error : " , error)
                return error
            return reg_id
    NewModel.__name__ = table_param
    return NewModel