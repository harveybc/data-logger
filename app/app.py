# -*- encoding: utf-8 -*-

from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import sys
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
import json

from flask import current_app, g
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
import base64
from app.util import load_plugin_config, reflect_prepare

#import prance

db = SQLAlchemy()
login_manager = LoginManager()


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
    import connexion
    app = connexion.App(__name__, specification_dir = specification_dir)
    # read the Connexion swagger yaml specification filename from the core plugin entry point
    specification_filename = data_logger.core_ep.specification_filename
    app.add_api(specification_filename)
    # set Flask static_folder  to be used with Connexion from the gui plugin entry point 
    static_url_path = data_logger.gui_ep.static_url_path
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
    #app.app.add_url_rule(app.app.static_url_path + '/<path:filename>',endpoint='static', view_func=app.app.send_static_file)
    #app.app.add_url_rule(app.app.static_url_path + '/<path:filename>',endpoint='/statical/assets', view_func=app.app.send_static_file)
    # read plugin configuration JSON file
    app.app.config.from_object(app_config)
    # initialize db with current app
    db.init_app(app.app)
    # initialize automap Base
    #reflect_prepare(db, Base)
    Base = automap_base()
    with app.app.app_context():
        Base.prepare(db.engine)
    # update the Base property of the core plugin entry point
    data_logger.core_ep.Base = Base
    # initialize login manager
    login_manager.init_app(app.app)
    # get the output plugin template folder
    plugin_folder = data_logger.gui_ep.template_path()
    # register the blueprints from the gui plugin
    data_logger.gui_ep.register_blueprints(app.app, data_logger.core_ep, data_logger.store_ep, db, Base)
    
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

    @app.app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
    return app.app

#def bundled_specs(main_file: Path) -> Dict[str, Any]:
#    parser = prance.ResolvingParser(str(main_file.absolute()),
#                                    lazy = True, backend = 'openapi-spec-validator')
#    parser.parse()
#    return parser.specs

