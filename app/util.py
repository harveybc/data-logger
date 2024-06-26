# -*- encoding: utf-8 -*-
""" Common functions """
 
import hashlib, binascii, os
import json
from sqlalchemy.ext.automap import automap_base
from inspect import currentframe, getframeinfo

def sanitize_str(insecure_str, max_len):
    """ Limits a string's length and removes insecure characters from it.

        Args:
        insecure_str (str): input string.
        max_len (int): maximum string length.

        Returns:
        secure_str (str): sanitized string.
    """
    # limit the length of the input_str  to 256 chars
    short_input = (insecure_str[:max_len]) if len(insecure_str) > max_len else insecure_str
    # remove dangerous characters
    secure_str = short_input.strip("\"',\\*.!:-+/ #\{\}[]")
    return secure_str

def load_plugin_config():
    print(" * Loading plugin configuration files")
    plugin_conf = {}
    try:
        with open("config_store.json", "r") as conf_file:
            plugin_conf['store'] = json.load(conf_file)
        with open("config_core.json", "r") as conf_file:
            plugin_conf['core'] = json.load(conf_file)
        with open("config_gui.json", "r") as conf_file:
            plugin_conf['gui'] = json.load(conf_file)
    except Exception as e:
        print(e)
        exit(e)
    return(plugin_conf)

def as_dict(model):   
    """ Convert to dict containing all the columns in this model

        Returns:
        r2 (dict): the model's columns as dict.
    """
    r2 = {}
    for c in model.__table__.columns:
        attr = getattr(model, c.name)
        if is_num(attr):
            r2[c.name]=attr
        else:
            r2[c.name]=str(attr)
    return r2

def reflect_prepare(db, Base):
    """ Update SQLAlchemy metadata and prepare automap base to allow ORM in all tables. """
    #update metadata and tables
    db.Model.metadata.reflect(bind=db.engine)
    # reflect the tables
    Base.prepare(db.engine, reflect=True)

def is_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False

def hash_pass( password ):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash) # return bytes

def verify_pass_ascii(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

# format error messages by preceding the filename and line number to the error message
def error_f(msg):
    cf = currentframe()
    return "File \"" + getframeinfo(cf.f_back).filename + "\", line " + str(cf.f_back.f_lineno) + " : " + msg  
