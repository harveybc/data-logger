from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flask_login import login_required
from flask_login import current_user
from app.db import get_db
from flask import current_app
from flask import jsonify
from app.app import load_plugin_config


def new_bp(plugin_folder, core_ep, store_ep, db, Base):

    # construct the data_logger blueprint using the plugin folder as template folder
    bp = Blueprint("configs_bp", __name__, template_folder=plugin_folder+"/templates")
    @bp.route("/configs")
    #@login_required
    def configs_index():
        """Show the configs index."""
        p_config = load_plugin_config()
        p_config_gui = p_config["gui"]
        return render_template("/configs/index.html", p_config=p_config_gui)
    
    @bp.route("/configs/gymfx_configs_list_")
    #@login_required
    def gymfx_configs_list():
        """returns the configs list as a text, from the core plugin"""
        configs_list = core_ep.ConfigsController.read_all(Base)
        return configs_list

    @bp.route("/views/configs")
    #@login_required
    def process_index():
        """Show the users index."""
        user_list = current_app.config['FE'].ep_input.get_users()
        return render_template("/plugin_templates/user/index.html", user_list = user_list)

    @bp.route("/views/configs/<username>")
    @login_required
    def process_detail(username):
        """Show the user detail view, if it is the current user, shows a change password button."""
        user_list = current_app.config['FE'].ep_input.get_user_by_username(username)
        return render_template("/plugin_templates/user/detail.html", user_list =  user_list, username = username)

 
    return bp
