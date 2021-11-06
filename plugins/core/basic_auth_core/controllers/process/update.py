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
from ...models.process_register_factory import ProcessRegisterFactory
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
            # replace model with body fields
            for property, value in body['process'].items():
                setattr(process_model, property, value) 
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_a' : error}
        # perform update 
        try:
            db.session.commit()
            #db.session.expunge_all()
            #db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_b' : error}
        # test if the model was updated 
        try:
            res['process'] = as_dict(Process.query.filter_by(id=int(process_id)).one())
            #db.session.expunge_all()
            #db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_c' : error}    
    # check if the process parameter is present    
    if 'register' in body:
        # instantiate process register with the body dict as kwargs
        ProcessRegister = ProcessRegisterFactory(body['register']['table'])
        res['register'] = ProcessRegister.update(**body['register'])
    # return register as dict
    return res
