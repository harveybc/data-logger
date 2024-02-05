""" Controller for the configs endpoints. 
    Description: Contains API endpoint handler functions for CRUD operations 
    on the logs table whose registers are an ordered set of rules
    that a request must approve to perform its intended action.
    
    By default, admin users can CRUD processes, tables and table registers.
    
    Also by default, all users can read/create registers on their processes' tables, 
    but can't create processes or tables, and can't update/delete registers.

    When logs are created for an user, process or a table
    the user, process or table is denied all access but the indicated.

    The list of logs for an user, process or table is ordered by the 
    priority column and the highest priority rules override the lowest priority ones.

"""

from app.app import db
import json
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from datetime import datetime
from app.app import login_manager
from ..models.authorization import Authorization
from ..models.process_table import ProcessTable
from ..models.process_register_factory import ProcessRegisterFactory
from sqlalchemy.ext.automap import automap_base
from .common import as_dict, is_num
from functools import wraps
from flask import (current_app)
from flask import request

class ConfigsController():
            
    #@authorization_required
    #@log_required
    def create(body, Base):
        """ Create a register in db based on a json from a request's body parameter.

            Args:
            body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

            Returns:
            res (dict): the newly created register.
        """
        # instantiate user with the body dict as kwargs
        ConfigsModel = ProcessRegisterFactory("gym_fx_config", Base)
        new = ConfigsModel(**body)
        # create new flask-sqlalchemy session
        db.session.add(new)
        try:
            db.session.commit()
            new_id =  new.id
            #db.session.expunge_all()
            #db.session.close()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print("Error: ", error)
            return error
        # test if the new user was created 
        try:
            res = ConfigsModel.query.filter_by(id=new_id).one()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print("Error: ", error)
            return error
        # return register as dict
        return as_dict(res)

    #@authorization_required
    def read(authorization_id, Base):
        """ Performs a query log register.

            Args:
            process_id (str): authorization_id (log/<authorization_id>).

            Returns:
            res (dict): the requested  register.
        """
        ConfigsModel = ProcessRegisterFactory("gym_fx_config", Base)
        try:
            res = as_dict(ConfigsModel.read(id=authorization_id))
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            return error 
        return res

    #@authorization_required
    #@log_required
    def update(authorization_id, body, Base):
        """ Update a register in db based on a json from a request's body parameter.

            Args:
            user_id (str): id field of the model, obtained from url parameter (log/<authorization_id>).
            body (dict): dict containing the fields of the register, obtained from json in the body of the request.

            Returns:
            res (dict): the updated register
        """
        # query the existing register
        ConfigsModel = ProcessRegisterFactory("gym_fx_config", Base)
        try:
            process_model = ConfigsModel.read(id=authorization_id)
            for property, value in body.items():
                setattr(process_model, property, value)
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            res = { 'error_a' : error}
        # replace model with body fields
        
        # perform update 
        try:
            db.session.commit()
            #db.session.expunge_all()
            #db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            res = { 'error_b' : error}
        # test if the model was updated 
        try:
            res = as_dict(ConfigsModel.read(id=int(authorization_id)))
            #db.session.expunge_all()
            #db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            res = { 'error_c' : error}
        return res

    #@authorization_required
    #@log_required
    def delete(authorization_id, Base):
        """ Delete a register in db based on the id field of the authorizarions model, obtained from a request's authorization_id url parameter.

            Args:
            process_id (str): id field , obtained from a request's url parameter (log/<authorization_id>).

            Returns:
            res (int): the deleted register id field
        """
        ConfigsModel = ProcessRegisterFactory("gym_fx_config", Base)
        try:
            res = ConfigsModel.getmodel(id=authorization_id).one()
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            return error
        # perform delete 
        db.session.delete(res)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            return error
        return { "id" : res.id }

    #@authorization_required
    def read_all(Base):
        """ Query all registers of the logs table.

            Returns:
            res (dict): the requested list.
        """ 
        ConfigsModel = ProcessRegisterFactory("gym_fx_config", Base)
        try:
            res = ConfigsModel.read_all()
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            return error
        # convert to list of dicts and empty pass
        res2 =[]
        for r in res:
            res2.append(as_dict(r))
        return res2
