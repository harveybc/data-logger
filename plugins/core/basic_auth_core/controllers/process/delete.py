""" Controller for the process endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""

from app.app import db
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from app.app import login_manager
from ...models.process import Process
from ...models.process_table import ProcessTable
from ...models.process_register_factory import ProcessRegisterFactory
from flask import request
from sqlalchemy.ext.automap import automap_base
from ...controllers.authorization import authorization_required
from ...controllers.log import log_required

@authorization_required
@log_required
def delete(process_id):
    """ Delete a register in db based on the id field of the process model, obtained from a request's process_id url parameter.

        Args:
        process_id (str): id field of the process model, obtained from a request's process_id url parameter (processs/<process_id>).

        Returns:
        res (int): the deleted register id field
    """ 
    table_param = request.args.get("table")
    # TODO: filter by userid and column,value
    # delete process
    if table_param is None:
        try:
            res = Process.query.filter_by(id=process_id).one()
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
        return res.id
    else:
        # parse the table_param string because eval is used
        #update metadata and tables
        # verify if the reg_id param is set
        reg_id = request.args.get("reg_id")
        # delete table
        if reg_id is None:
            return ProcessTable.delete(process_id, table_param)
        # delete register
        else:
            ProcessRegister = ProcessRegisterFactory(table_param)
            return ProcessRegister.delete(process_id, table_param, reg_id)

            
