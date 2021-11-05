# -*- encoding: utf-8 -*-

from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import sys
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
import json
import connexion
from flask import current_app, g
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
import base64
from app.util import load_plugin_config
#import prance

db = SQLAlchemy()
login_manager = LoginManager()
Base = automap_base()

def create_app(app_config, data_logger):
    """ Create the Flask-Sqlalchemy app 
    Args:
    app_config (dict): flask app config data
    data_logger (obj): DataLogger class instance

    Returns:
    app.app (dict): the flask-sqlalchemy app instance
    """    

    # read the Connexion swagger yaml specification_dir from the core plugin entry point
    specification_dir = data_logger.core_ep.specification_dir
    app = connexion.App(__name__, specification_dir = specification_dir)
    # read the Connexion swagger yaml specification filename from the core plugin entry point
    specification_filename = data_logger.core_ep.specification_filename
    #app.add_api('DataLogger-OAS.apic.yaml')
    app.add_api(specification_filename)
    # set Flask static_folder  to be used with Connexion from the gui plugin entry point 
    static_url_path = data_logger.gui_ep.static_url_path
    #app.app.static_url_path = '/base/static'
    app.app.static_url_path = static_url_path
    # remove old static map
    url_map = app.app.url_map
    try:
        for rule in url_map.iter_rules('static'):
            url_map._rules.remove(rule)
    except ValueError:
        # no static view was created yet
        pass
    # adds an url rule to serve static files from the gui plugin location
    app.app.add_url_rule(app.app.static_url_path + '/<path:filename>',endpoint='static', view_func=app.app.send_static_file)
    # read plugin configuration JSON file
    #p_config = read_plugin_config()
    # initialize FeatureExtractor
    ###fe = FeatureExtractor(p_config)
    # set flask app parameters
    app.app.config.from_object(app_config)
    # plugin configuration from data_logger.json
    #app.app.config['P_CONFIG'] = p_config 
    # data_logger instance with plugins already loaded
    ### current_app.config['FE'] = fe
    db.init_app(app)
    login_manager.init_app(app)
    # get the output plugin template folder
    plugin_folder = data_logger.gui_ep.template_path()
    # register the blueprints from the gui plugin
    data_logger.gui_ep.register_blueprints(app.app, data_logger.core_ep )
    
    # create User model for login manager
    User = data_logger.core_ep.User
    @login_manager.user_loader
    def user_loader(id):
        return User.query.filter_by(id=id).first()

    @login_manager.request_loader
    def load_user_from_request(request):
        # login using Basic Auth
        credentials = request.headers.get('Authorization')
        if credentials:
            credentials = credentials.replace('Basic ', '', 1)
            try:
                credentials = base64.b64decode(credentials)
            except TypeError:
                pass
            cred_list = credentials.decode().split(':')
            username = cred_list[0]
            password = cred_list[1]
            user = User.query.filter_by(username=username).first()
            if user:
                return user
        # return None if user is not logged in
        return None

    # If it is the first time the app is run, create the database and perform data seeding
    #@app.app.before_first_request
        #print("tables=", db.metadata.tables)
    #    @app.before_first_request
    #    def initialize_database():
    #        pass
    #    @app.teardown_request
    #    def shutdown_session(exception=None):
    #        db.session.remove()

    @app.app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
    
    return app.app


#def bundled_specs(main_file: Path) -> Dict[str, Any]:
#    parser = prance.ResolvingParser(str(main_file.absolute()),
#                                    lazy = True, backend = 'openapi-spec-validator')
#    parser.parse()
#    return parser.specs
