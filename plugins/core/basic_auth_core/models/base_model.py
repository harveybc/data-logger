""" Base Model. 
    Description: Contains common methods for all models so they can use ORM.
""" 
import datetime
from app.util import hash_pass, reflect_prepare
from app.app import login_manager
from sqlalchemy.exc import SQLAlchemyError
from app.app import db
from sqlalchemy.ext.automap import automap_base

class BaseModel():
    """ Base class for the data_logger models 
        
        Args:
        db.Model (SQLAlchemy Model): SQLAlchemy declarative base extension model to tallow ORM.

        Description: Contains methods to operate in the database without authorization or logging, meant to be called from the controllers that implement the API endpoints with AAA.
        Also contains other common methods for data_logger models.
    """
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if isinstance(value, list) or isinstance(value, tuple):
                if len(value) == 1:
                    if  not isinstance(value, str) and not isinstance(value, dict):
                        value = value[0]
            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
            setattr(self, property, value)
        # initializes automap base class that allows ORM in all tables
        reflect_prepare(db, self)
    
    @classmethod
    def create(cls, **body): 
        """ Create a register in db based on a json from a request's body parameter.

            Args:
            body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

            Returns:
            res (model): the newly created model.
        """
        # instantiate user with the body dict as kwargs
        res = cls(**body)
        # create new flask-sqlalchemy session
        db.session.add(res)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
        return res

    @classmethod
    def read_all(cls):
        """ Query all models.

            Returns:
            res [(model)]: list of models.
        """ 
        try:
            res = cls.query.all()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
        return res
        
    @classmethod
    def read(cls, Id):
        """ Query a register in db based on the id field of the model.

            Args:
            Id (Integer): id attribute of the model.

            Returns:
            res (model): the requested model.
        """ 
        try:
            res = cls.query.filter_by(id=Id).first_or_404()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
        return res

    @classmethod
    def update(cls, body, Id):
        """ Update a register in db based on a json from a request's body parameter.

            Args:
            Id (str): id field of the  model.
            body (dict): dict containing the fields of the register to be updated.

            Returns:
            res (dict): the updated model with empty password field.
        """
        # query the existing register
        try:
            res = cls.query.filter_by(id=Id).first_or_404()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
        # replace model with body fields
        res = cls(**body)
        res.id =  Id
        # set the updated model as modified for update. Use flag_modified to flag a single attribute change.
        db.session.merge(res)
        # perform update 
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
        return res

    @classmethod
    def delete(cls, Id):
        """ Delete a register in db based on the id field of the model.

            Args:
            userId (str): id field of the model.

            Returns:
            res (int): the deleted register id field
        """ 
        try:
            res = cls.query.filter_by(id=Id).first_or_404()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
        # perform delete 
        db.session.delete(res)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
        return Id
