""" Map this model's fields and relationships """

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, MetaData, Table
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
            print("\nc=",c)
            if "primary_key" in c:
                if c["primary_key"]:
                    t_args.append(Column(c["name"], eval(c["col_type"]), primary_key=c["primary_key"], autoincrement=True, nullable=False))
            elif "foreign_key" in c:
                if c["foreign_key"] != "none":
                    t_args.append(Column(c["name"], eval(c["col_type"]), ForeignKey(c["foreign_key"]), unique=c["unique"], index=c["index"], default=c["default"], nullable=c["nullable"]))
            else:
                t_args.append(Column(c["name"], eval(c["col_type"]), primary_key=False, unique=c["unique"], index=c["index"], default=c["default"], nullable=c["nullable"]))
        # instance the Table class with the t_args
        metadata=MetaData()
        self.table = Table(autoload_with=db.engine, *t_args)

    def __repr__(self):
        return str(self.name)

