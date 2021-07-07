""" Controller for the process endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""

from app.app import db
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from app.app import login_manager
from models.process import Process
from flask import request
from sqlalchemy.ext.automap import automap_base
from controllers.authorization import authorization_required
from controllers.log import log_required

@authorization_required
@log_required
def delete(processId):
    """ Delete a register in db based on the id field of the process model, obtained from a request's processId url parameter.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).

        Returns:
        res (int): the deleted register id field
    """ 
    

    table_param = request.args.get("table")
    # query a process model 
    # TODO: filter by userid and column,value
    if table_param is None:
        try:
            res = Process.query.filter_by(id=processId).one()
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
    else:
        # parse the table_param string because eval is used
        table_param = table_param.strip("\"',\\*.!:-+/ #\{\}[]")
        Base = automap_base()
        #update metadata and tables
        Base.prepare(db.engine, reflect=True)
        register_model = eval("Base.classes." + table_param)
        # verify if the reg_id param is set
        reg_id = request.args.get("reg_id")
        if reg_id is None:
            # TODO: verify that the table is in the tables array of the current process
            # delete the table
            try:
                register_model.__table__.drop(db.engine)
                db.session.commit()
                return table_param + " table deleted"
            except SQLAlchemyError as e:
                error = str(e)
                return error
        else:
            # perform query
            try:
                res=db.session.query(register_model).filter_by(id=reg_id).one()
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
            
