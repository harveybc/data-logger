""" Controller for the process endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""

from app.app import db, engine
import json
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from datetime import datetime
from app.app import login_manager
from models.process import Process
from models.process_table import ProcessTable
from models.process_register import ProcessRegister
from sqlalchemy import Table, insert


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
            return error
        # TODO: Remove the following and return the same input instead of confirming (nah)?
        # test if the new process was created 
        try:
            res['process'] = Process.query.filter_by(name=new_process.name).first_or_404().as_dict()
        except SQLAlchemyError as e:
            error = str(e)
            return error
        # return register as dict
    # use kwargs to check if the process parameter is present    
    if 'table' in body:
        # instantiate process table with the body dict as kwargs
        new_table = ProcessTable(**body['table'])
        if not db.engine.dialect.has_table(db.engine, new_table.name):
            new_table.table.create(db.engine)
        # test if the new process table  was created 
        try:
            if db.engine.dialect.has_table(db.engine, new_table.name):
                cols = db.metadata.tables[new_table.name].c
                r_table={}
                r_table['name'] = new_table.name
                r_table['columns'] = [column.key for column in cols]               
                res['table'] = r_table
        except SQLAlchemyError as e:
            error = str(e)
            return error
        # return register as dict
        return res
    # use kwargs to check if the process parameter is present    
    if 'register' in body:
        # instantiate process register with the body dict as kwargs
        new_register = ProcessRegister(**body['register'])
        # create the register
        try:
            # verify if table exists
            if db.engine.dialect.has_table(db.engine, new_table.name):
                # execute new_register statement in engine
                result_proxy = engine.execute(new_register.stmt)
                res['register'] = result_proxy
        except SQLAlchemyError as e:
            error = str(e)
            return error
        # return register as dict
        return res
    
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
    """ Query all registers of the process model.

        Returns:
        res (dict): the requested process registers with empty password field.
    """ 
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
   




