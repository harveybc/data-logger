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
from sqlalchemy import Table, insert
from sqlalchemy.ext.automap import automap_base
from flask import request
import controllers.process_table as ptable

@login_required
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
    # use kwargs to check if the process parameter is present
    if 'process' in body:
        # create new table
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
            res['process'] = { 'error' : error}
        # TODO: Remove the following and return the same input instead of confirming (nah)?
        # test if the new process was created 
        try:
            res['process'] = Process.query.filter_by(name=new_process.name).first_or_404().as_dict()
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] ={ 'error' : error}
    # use kwargs to check if the process parameter is present    
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
            p_table = Process.query.filter_by(id=new_table.process_id).first_or_404().as_dict()
        except SQLAlchemyError as e:
            error = str(e)
            return error
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
        db.session.add(Process(**p_table))
        try:
            #db.session.commit()
            db.session.close()
            pass
        except SQLAlchemyError as e:
            error = str(e)
            res['process'] ={ 'error' : error}
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
    
def row2dict(resultproxy):
    d, a = {}, []
    for rowproxy in resultproxy:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d = {**d, **{column: value}}
        a.append(d)
    return a

def read(processId):
    """ Query a register in db based on the id field of the process model, obtained from a request's processId url parameter.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).

        Returns:
        res (dict): the requested process register with empty password field.
    """ 
    try:
        res = Process.query.filter_by(name=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # empty pass
    res.password=""
    return res.as_dict()
    

def update(processId, body):
    """ Update a register in db based on a json from a request's body parameter.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created process register with empty password field.
    """
    # query the existing register
    try:
        res = Process.query.filter_by(name=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # replace model with body fields
    body['id']=res.id
    res.__dict__ = body
    # perform update 
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # test if the model was updated 
    try:
        res = Process.query.filter_by(name=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # empty pass
    res.password=""
    # return register as dict
    return res.as_dict()

def delete(processId):
    """ Delete a register in db based on the id field of the process model, obtained from a request's processId url parameter.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).

        Returns:
        res (int): the deleted register id field
    """ 
    try:
        res = Process.query.filter_by(name=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    # perform delete 
    db.session.delete(res)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e)
        return error
    return res.id

def read_all():
    """ Query all registers of the process, process table or process register.

        Returns:
        res (dict): the requested process registers with empty password field.
    """ 
    # check if the "process" url param is set (either generate the list of tables or registers in a table) else, generate a list of processes
    process_param = request.args.get("process")
    # generate the list of processes 
    # TODO: filter by userid and column,value
    if process_param is None:
        try:
            res = Process.query.all()
        except SQLAlchemyError as e:
            error = str(e)
            return error
        # convert to list of dicts and empty pass
        res2 =[]
        for r in res:
            r.password = ""
            res2.append(r.as_dict())
        return res2
    # if the process url param is present, either generate a list of tables or a list of registers of a table
    else:
        table_param = request.args.get("table")
        # generate the list of tables 
        # TODO: filter by userid and column,value
        if table_param is None:
            try:
                # TODO: get tables array from the process
                #ptable.read_all(int(process_param))
                proc = Process.query.filter_by(id=int(process_param)).first_or_404()
                res = proc.tables
            except SQLAlchemyError as e:
                error = str(e)
                return error
            return res