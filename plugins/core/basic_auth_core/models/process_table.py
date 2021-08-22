""" Model and crud model functions for the process tables"""

from sqlalchemy import Column, ForeignKey, MetaData, Table, BigInteger, Boolean, Date, DateTime, Enum, Float, Integer, Interval, LargeBinary, Numeric, PickleType, SmallInteger, String, Text, Time, Unicode, UnicodeText
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from app.util import sanitize_str, reflect_prepare
from pydoc import locate 
from copy import deepcopy
from sqlalchemy.ext.automap import automap_base
from ..models.process import Process
import json
from sqlalchemy.exc import SQLAlchemyError
from ..controllers.common import as_dict, is_num

class ProcessTable():
    """ Map the columns to a list of Table constructor arguments """
    def __init__(self, **kwargs):
        # extract kwargs into class attributes
        for property, value in kwargs.items():
        #    print(property, " = ", value)
            setattr(self, property, value)
        # initialize Table class parameters list
        t_args = []
        # add the name
        t_args.append(self.name)
        # add metadata 
        t_args.append(db.metadata)
        # add columns and search if there is a primary key and/or timestamp defined 
        pk_found = False
        timestamp_found = False
        id_found = False
        for c in self.columns:
            # assign default values to each column parameter if it does not exist 
            if "unique" not in c: c["unique"] = False
            if "index" not in c: c["index"] = False
            if "default" not in c: c["default"] = {}
            if "nullable" not in c: c["nullable"] = False
            # generate the arguments for this column
            if "col_type" not in c: c["col_type"] = "Float"
            col_type = self.parse_sqlalchemy_column_type(c["col_type"])
            if "primary_key" in c:
                if c["primary_key"]:
                    t_args.append(Column(c["name"], col_type, autoincrement=True, primary_key=c["primary_key"], nullable=False))
                    pk_found = True
            if "foreign_key" in c:
                if c["foreign_key"] != "none":
                    t_args.append(Column(c["name"], col_type, ForeignKey("p_schema." + c["foreign_key"]), unique=c["unique"], index=c["index"], default=c["default"], nullable=c["nullable"]))
            if "primary_key" not in c and "foreign_key" not in c:
                t_args.append(Column(c["name"], col_type, primary_key=False, unique=c["unique"], index=c["index"], default=c["default"], nullable=c["nullable"]))
            if c["name"] == "timestamp":
                timestamp_found = True
            if c["name"] == "id":
                id_found = True
        # create a new id column if a primary key was not found
        if not pk_found and not id_found:
            t_args.append(Column("id", col_type, autoincrement=True, primary_key=True, nullable=False))
        # create a new timestamp column if it was not found
        if not timestamp_found:
            t_args.append(Column("timestamp", String, server_default=str(datetime.now())))
        # instance the Table class with the t_args
        self.table = Table(*t_args, extend_existing=True)
    
    # ensures the type is a single word representing the sqlalchemy type of the columns
    def parse_sqlalchemy_column_type(self, input_str):
        # sanitize the input string and limit its length
        translated_input = sanitize_str(input_str, 256)
        valid_types = [
            translated_input == "BigInteger", translated_input == "Boolean", translated_input == "Date", translated_input == "DateTime", translated_input == "Enum", 
            translated_input == "Float", translated_input == "Integer", translated_input == "Interval", translated_input == "LargeBinary", translated_input == "MatchType", 
            translated_input == "Numeric", translated_input == "PickleType", translated_input == "SchemaType", translated_input == "SmallInteger", translated_input == "String", 
            translated_input == "Text", translated_input == "Time", translated_input == "Unicode", translated_input == "UnicodeText"
        ]
        if any(valid_types):
            return eval(translated_input)
        else:
            return Integer

    def __repr__(self):
        return str(self.name)

    @classmethod
    def create(cls, **table_dict): 
        """ Create a table.
        
            Args:
            body (dict): dict containing the fields of the new table.

            Returns:
            res (dict): the process containing the new table.
        """
        #initialize void response
        res = {}
        # instantiate process table with the body dict as kwargs
        #table = deepcopy(table_dict)
        cls = cls(**table_dict)
        for attr, value in cls.__dict__.items():
            print(attr, value)
        if not db.engine.dialect.has_table(db.engine, cls.name):
            cls.table.create(db.engine)
        #update metadata and tables
        reflect_prepare(cls)
        # add the table to the tables array in the process (convert to string for compatibility)
        try:
            p_model = Process.query.filter_by(id=cls.process_id).one()
            p_table = as_dict(p_model)
            # construct a table model (see swagger yaml) with table_column models
            table_m = {}
            table_m["name"] = cls.name
            # TODO: verify if its neccesary to have the real_name attribute or of is required to use a prefix
            table_m["real_name"] = cls.name
            table_m["columns"] = cls.columns
            # convert the tables string to an array
            t_array = json.loads(p_table["tables"])
            #insert the new table model in the tables array
            t_array.append(table_m)
            # save the table_m array in a json string in process.tables 
            p_table["tables"] = json.dumps(t_array)
            # update the tables attribute in the process model
            p_model.tables = p_table["tables"] 
            db.session.commit()
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res = { 'error_c' : error}
            return res
        return p_table
        
    @classmethod            
    def read(cls, process_id, table_param):
        """ Performs a query to a process table.

            Args:
            process_id (str): id field of the process model.

            table_param (str): name of the table 

            Returns:
            res (dict): the requested process table.
        """ 
        # query a process model 
        # TODO: filter by userid and column,value
        # sanitize the input string and limit its length
        table_param = sanitize_str(table_param, 256)
        # query a table
        try:
            # TODO: query table by name from process tables array 
            #ptable.read_all(int(process_param))
            proc = as_dict(Process.query.filter_by(id=process_id).one())
            res_list = json.loads(proc["tables"])
        except SQLAlchemyError as e:
            error = str(e)
            return error
        # search for the name in the keys of elements of  the tables array.       
        try:
            return next(x for x in res_list if table_param in x["name"])
        except StopIteration:
            raise ValueError("No matching record found")     
            return None

    @classmethod
    def read_all(cls, process_id):
        """ Query all tables of a process.
            
            Args:
            process_id (str): id field of the process model.
            
            Returns:
            res (list): the requested list of tables.
        """ 
        try:
            # TODO: get tables array from the process
            #ptable.read_all(int(process_param))
            proc = Process.query.filter_by(id=int(process_id)).first_or_404()
            res = json.loads(proc.tables)
        except SQLAlchemyError as e:
            error = str(e)
            return error
        return res

    @classmethod
    def delete(cls, process_id, table_param):
        """ Delete a table from a process.

            Args:
            process_id (str): id field of the process.

            table_param (str): name of the table

            Returns:
            res (str): table deleted confirmation message
        """ 
        # query a process model 
        # TODO: filter by userid and column,value
        Base = automap_base()
        #update metadata and tables
        Base.prepare(db.engine, reflect=True)
        # sanitize the input string and limit its length
        table_param = sanitize_str(table_param, 256)
        register_model = eval("Base.classes." + table_param)
        # TODO: verify that the table is in the tables array of the current process
        # delete the table
        try:
            register_model.__table__.drop(db.engine)
            reflect_prepare(cls)
            return table_param + " table deleted"
        except SQLAlchemyError as e:
            error = str(e)
            return error