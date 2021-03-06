""" Controller for the process endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""

from app.app import db
import json
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from datetime import datetime
from app.app import login_manager
from ...models.process import Process
from ...models.process_table import ProcessTable
from ...models.process_register import ProcessRegister
from sqlalchemy.ext.automap import automap_base
from ...controllers.common import as_dict, is_num
from ...controllers.authorization import authorization_required
from ...controllers.log import log_required

@authorization_required
@log_required
def update(process_id, body):
    """ Update a register in db based on a json from a request's body parameter.

        Args:
        process_id (str): id field of the process model, obtained from a request's process_id url parameter (processs/<process_id>).
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
            process_model = Process.query.filter_by(id=process_id).one()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_a' : error}
        # replace model with body fields
        for property, value in body['process'].items():
            setattr(process_model, property, value)
        # perform update 
        try:
            db.session.commit()
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_b' : error}
        # test if the model was updated 
        try:
            res['process'] = Process.query.filter_by(id=int(process_id)).one().as_dict()
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_c' : error}
    
    # check if the process parameter is present    
    if 'register' in body:
        # instantiate process register with the body dict as kwargs
        #new_register = ProcessRegister(**body['register'])
        
        # query a table register
        Base = automap_base()
        #update metadata and tables
        Base.prepare(db.engine, reflect=True)
        register_model = eval("Base.classes." + body['register']['table'])
        # perform query
        model = db.session.query(register_model).filter_by(id=body['register']['reg_id']).one()
        # set the new values from the values array
        for property, value in body['register']['values'].items():
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
            res['register'] = as_dict(db.session.query(register_model).filter_by(id=body['register']['reg_id']).one())
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['register'] ={ 'error_e' : error}
        
    # return register as dict
    return res
