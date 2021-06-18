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
    #initialize void response
    res = {}
    # check if the process parameter is present
    if 'process' in body:
        # query the existing register
        try:
            res = Process.query.filter_by(name=processId).first_or_404()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_a' : error}
        # replace model with body fields
        body['id']=res.id
        res.__dict__ = body
        # perform update 
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_b' : error}
        # test if the model was updated 
        try:
            res['process'] = Process.query.filter_by(name=processId).first_or_404().as_dict()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_a' : error}
        
    if "process" in res:
            res['process']["tables"] = p_table["tables"]
            
        # test if the new process table  was created 
        try:
            if db.engine.dialect.has_table(db.engine, new_table.name):
                cols = db.metadata.tables[new_table.name].c
                r_table={}
                r_table['name'] = new_table.name
                r_table['columns'] = [column.key for column in cols]               
                res['table'] = r_table
            else:
                res['table'] = {}
        except SQLAlchemyError as e:
            error = str(e)
            res['table'] ={ 'error' : error}
    # use kwargs to check if the process parameter is present    
    if 'register' in body:
        # instantiate process register with the body dict as kwargs
        new_register = ProcessRegister(**body['register'])
        # create the register
        try:
            # verify if table exists
            if db.engine.dialect.has_table(db.engine, new_register.table):
                # execute new_register statement in engine
                result_proxy = db.engine.execute(new_register.stmt)
                res['register'] = {"result" : "ok"}
            else:
                res['register'] = {"result": "table does not exists"}
        except SQLAlchemyError as e:
            error = str(e)
            res['register'] ={ 'error' : error}
        # return register as dict
        return res
