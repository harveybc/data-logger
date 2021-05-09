""" Map this model's fields and relationships """
    
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from app.app import db
import datetime
from sqlalchemy.orm import relationship

class Process(db.Model):
    """ Map the process table columns and bidirectional one-to-many relationship with user """
    __tablename__ = 'process'

    # columns
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    tables=Column(String)
    created=Column(DateTime, default=datetime.datetime.utcnow)
    user_id=Column(Integer, ForeignKey('user.id'))

    # relationships
    user = relationship("User", back_populates='processes')

    def __repr__(self):
        return str(self.name)




