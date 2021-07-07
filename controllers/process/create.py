""" Controller for the process/create endpoint. 
    Description: Contains API endpoint handler functions for create proces, process table or process table registers.  
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
from controllers.authorization import authorization_required
from controllers.log import log_required

@log_required
@authorization_required
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
        # create new process
        new_process = Process(**body['process'])
        # set user_id same as the requesting user
        #new_process.user_id = current_user
        new_process.user_id = current_user.get_id()
        # transform the tables json into string
        new_process.tables = json.dumps(new_process.tables)
        # set the string date into datetime
        # new_process.created = datetime.strptime(new_process.created, '%Y-%m-%d  %H:%M:%S.%f')
        new_process.created = str(datetime.now())
        # add the modified process to the session
        db.session.add(new_process)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] = { 'error_a' : error}
        # TODO: Remove the following and return the same input instead of confirming (nah)?
        # test if the new process was created 
        try:
            res['process'] = Process.query.filter_by(name=new_process.name).one().as_dict()
#            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] ={ 'error_b' : error}
    # check if the table parameter is present    
    if 'table' in body:
        # instantiate process table with the body dict as kwargs
        new_table = ProcessTable(**body['table'])
        if not db.engine.dialect.has_table(db.engine, new_table.name):
            new_table.table.create(db.engine)
        #update metadata and tables
        db.Model.metadata.reflect(bind=db.engine)
        # reflect the tables
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)
        
        # add the table to the tables array in the process (convert to string for compatibility)
        try:
            p_model = Process.query.filter_by(id=new_table.process_id).one()
            p_table = p_model.as_dict()
            # construct a table model (see swagger yaml) with table_column models
            table_m = {}
            table_m["name"] = new_table.name
            # TODO: verify if its neccesary to have the real_name attribute or of is required to use a prefix
            table_m["real_name"] = new_table.name
            table_m["columns"] = new_table.columns
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
            res['table'] ={ 'error_c' : error}
            return res
        # update  the output in case the table was created in the same request as the process
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
            res['table'] ={ 'error_d' : error}
            return res
    # check if the process parameter is present    
    if 'register' in body:
        # instantiate process register with the body dict as kwargs
        #new_register = ProcessRegister(**body['register'])
        # query a table register
        Base = automap_base()
        #update metadata and tables
        Base.prepare(db.engine, reflect=True)
        register_base = eval("Base.classes." + body['register']['table'])
        # set the new values from the values array
        register_model = register_base(**body['register']['values'])
        # update the register
        try:
            db.session.add(register_model)
            db.session.commit()
            new_id = register_model.id
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['register'] ={ 'error_d' : error}
        # verify if the register was created
        try:
            res['register'] = as_dict(db.session.query(register_base).filter_by(id=new_id).one())
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['register'] ={ 'error_e' : error}
        # return register as dict
    return res
