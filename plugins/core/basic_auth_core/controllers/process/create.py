""" Controller for the process/create endpoint. 
    Description: Contains API endpoint handler functions for create proces, process table or process table registers.  
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
from copy import deepcopy
from ...models.process_table import ProcessTable

@authorization_required
@log_required
def create(body): 
    """ Create a register in db based on a json from a request's body parameter.
		Also create the the process' tables based on the configuration field.

        Args:
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created process register with empty password field.
    """
    #initialize void response
    res = {}
    # check if the process parameter is present
    if 'process' in body:
        # set user_id same as the requesting user
        body["process"]["user_id"] = current_user.get_id()
        # transform the tables json into string
        if "tables" not in body["process"]:
            body["process"]["tables"] = "[]"
        # set the string date into datetime
        body["process"]["created"] = str(datetime.now())
        # create new process
        new_process = Process.create(**body['process'])
        # test if the new process was created 
        try:
            res['process'] = as_dict(Process.query.filter_by(name=new_process.name).one())
#            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] ={ 'error_b' : error}
    # check if the table parameter is present    
    if 'table' in body:
        # instantiate process table with the body dict as kwargs
        p_table = ProcessTable.create(**body["table"])
        # update  the output in case the table was created in the same request as the process
        if "process" in res:
            res['process']["tables"] = p_table["tables"]    
        # test if the new process table  was created 
        try:
            if db.engine.dialect.has_table(db.engine, body["table"]["name"]):
                cols = db.metadata.tables[body["table"]["name"]].c
                r_table={}
                r_table['name'] = body["table"]["name"]
                r_table['columns'] = [column.key for column in cols]               
                res['table'] = r_table
            else:
                res['table'] = {}
        except SQLAlchemyError as e:
            error = str(e)
            res['table'] ={ 'error_d' : error}
            return res
    # check if the process register parameter is present    
    if 'register' in body:
        register_model = ProcessRegisterFactory(body['register']['table'])    
        register_instance = register_model.create(**body['register'])    
        # return register as dict
        res['register']=register_instance

    return res
