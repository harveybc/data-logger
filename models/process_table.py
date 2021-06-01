""" Map this model's fields and relationships """

from sqlalchemy import Column, ForeignKey, MetaData, Table, BigInteger, Boolean, Date, DateTime, Enum, Float, Integer, Interval, LargeBinary, Numeric, PickleType, SmallInteger, String, Text, Time, Unicode, UnicodeText
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from pydoc import locate 


class ProcessTable():
    """ Map the columns to a list of Table constructor arguments """
    def __init__(self, **kwargs):
        # extract kwargs into class attributes
        for property, value in kwargs.items():
            setattr(self, property, value)
        # initialize Table class parameters list
        t_args = []
        # add the name
        t_args.append(self.name)
        # add metadata 
        t_args.append(db.metadata)
        # add columns 
        #TODO: PARSE COL_TYPE, BECAUSE EVAL IS USED
        for c in self.columns:
            # assign default values to each column parameter if it does not exist 
            if "unique" not in c: c["unique"] = False
            if "index" not in c: c["index"] = False
            if "default" not in c: c["default"] = {}
            if "nullable" not in c: c["nullable"] = False
            # generate the arguments for this column
            col_type = self.parse_sqlalchemy_column_type(c["col_type"])
            if "primary_key" in c:
                if c["primary_key"]:
                    t_args.append(Column(c["name"], col_type, autoincrement=True, primary_key=c["primary_key"], nullable=False))
            if "foreign_key" in c:
                if c["foreign_key"] != "none":
                    t_args.append(Column(c["name"], col_type, ForeignKey("p_schema." + c["foreign_key"]), unique=c["unique"], index=c["index"], default=c["default"], nullable=c["nullable"]))
            if "primary_key" not in c and "foreign_key" not in c:
                t_args.append(Column(c["name"], col_type, primary_key=False, unique=c["unique"], index=c["index"], default=c["default"], nullable=c["nullable"]))
        # instance the Table class with the t_args
        self.table = Table(*t_args, extend_existing=True)

    # ensures the type is a single word representing the sqlalchemy type of the columns
    def parse_sqlalchemy_column_type(self, input_str):
        # TODO: limit the length of the input_str 
        # remove dangerous characters
        translated_input = input_str.strip(chars="\"',\\*.!:-+/ #\{\}[]")
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

