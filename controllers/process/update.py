""" Controller for the process endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""

from app.app import db
import json
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from datetime import datetime
from app.app import login_manager
from models.process import Process
from models.process_table import ProcessTable
from models.process_register import ProcessRegister
from sqlalchemy.ext.automap import automap_base
from controllers.common import as_dict, is_num

@login_required
def update(processId, body):
    """ Update a register in db based on a json from a request's body parameter.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created process register with empty password field.
    """    
    # initialize void response
    res = {}
    # check if the process parameter is present
    if 'process' in body:
        # query the existing register
        try:
            process = Process.query.filter_by(id=processId).one()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_a' : error}
        # replace model with body fields
        body['process']['id']=processId
        process.__dict__ = body['process']
        # perform update 
        try:
            db.session.commit()
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_b' : error}
        # test if the model was updated 
        try:
            res['process'] = Process.query.filter_by(id=int(processId)).one().as_dict()
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_c' : error}
    
    # check if the process parameter is present    
    if 'register' in body:
        # instantiate process register with the body dict as kwargs
        new_register = ProcessRegister(**body['register'])
        
        # query a table register
        Base = automap_base()
        #update metadata and tables
        Base.prepare(db.engine, reflect=True)
        register_model = eval("Base.classes." + new_register.table)
        # perform query
        model = db.session.query(register_model).filter_by(id=new_register.reg_id).one()
        # set the new values from the values array
        print("new_register.values = ", new_register.values)
        for property, value in new_register.values:
            setattr(model, property, value)
        # update the register
        try:
            db.session.commit()
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['register'] ={ 'error_d' : error}
        # verify if the register was updated
        try:
            res['register'] = as_dict(db.session.query(register_model).filter_by(id=new_register.reg_id).one())
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['register'] ={ 'error_e' : error}
        
    # return register as dict
    return res
