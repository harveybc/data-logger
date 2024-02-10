
# This file contains the data_logger plugin, th input plugin can load all the data or starting from
 # the last id.

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
from app.util import as_dict
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, asc, desc
import json


def new_bp(plugin_folder, core_ep, store_ep, db, Base):

    # construct the data_logger blueprint using the plugin folder as template folder
    bp = Blueprint("dashboard_bp", __name__, template_folder=plugin_folder+"/templates")
    
    @bp.route("/")
    #@login_required
    def index():
        # read the data to be visualized using the using the Feature extractor instance, preinitialized in __init__.py with input and output plugins entry points.
        # TODO: replace 0 in vis_data by process_id, obtained as the first_or_404 process_id belonging to the current user.    
        # vis_data = current_app.config['FE'].ep_input.load_data(current_app.config['P_CONFIG'], 0)
        box= []
        #print("user_id = ", current_user.id)
        #box.append(current_app.config['FE'].ep_input.get_max(current_user.id, "training_progress", "mse"))
        #box.append(current_app.config['FE'].ep_input.get_max(current_user.id, "validation_stats", "mse"))
        #box.append(current_app.config['FE'].ep_input.get_count("user"))
        #box.append(current_app.config['FE'].ep_input.get_count("process"))
        ##TODO: Usar campo y tabla configurable desde JSON para graficar
        #v_original = current_app.config['FE'].ep_input.get_column_by_pid("validation_plots", "original", box[0]['id'] )
        #v_predicted = current_app.config['FE'].ep_input.get_column_by_pid("validation_plots", "predicted", box[0]['id'] )
        #p,t,v = current_app.config['FE'].ep_input.processes_by_uid(current_user.id)
        #tr_data = current_app.config['FE'].ep_input.training_data("trainingprogress", "mse")
        status = []
        #for i in range(0,len(p)):
        #    print ("v[i]['mse'] = ", v[i]['mse'])
        #    print ("t[i]['mse'] = ", t[i]['mse'])
        #    if v[i]['mse'] == None and t[i]['mse'] == None:
        #        status.append("Not Started")
        #        v[i]['MAX(mse)'] = 0.0
        #    elif v[i]['mse'] != None and t[i]['mse'] != None:
        #        status.append("Validation")           
        #    elif v[i]['mse'] == None and t[i]['mse'] != None: 
        #        v[i] = t[i]
        #        status.append("Training")
        #    print("status[",i,"] = ", status[i])
        #return render_template("/dashboard/index.html", p_config = current_app.config['P_CONFIG'], box = box, v_original = v_original, v_predicted = v_predicted, p=p, v=v, status=status)
        p_config = load_plugin_config()
        return render_template("/dashboard/index.html", p_config = p_config["gui"], p_config_store = p_config["store"])

    @bp.route("/dashboard/plots")
    #@login_required
    def plots_index():
        """Show the plot list."""
        p_config = load_plugin_config()
        return render_template("/dashboard/plots.html", p_config = p_config["gui"], p_config_store = p_config["store"])
    
    @bp.route("/dashboard/training")
    #@login_required
    def training_index():
        """Show the training stats."""
        p_config = load_plugin_config()
        p_config_gui = p_config["gui"]
        return render_template("/dashboard/training.html", p_config = p_config_gui)

    @bp.route("/dashboard/validation")
    #@login_required
    def validation_index():
        """Show the validation stats."""
        p_config = load_plugin_config()
        p_config_gui = p_config["gui"]
        return render_template("/dashboard/validation.html", p_config = p_config_gui)
    
    @bp.route("/dashboard/logs")
    #@login_required
    def log_index():
        """Show the logs index."""
        p_config = load_plugin_config()
        p_config_gui = p_config["gui"]
        return render_template("/dashboard/log.html", p_config=p_config_gui)

    def get_xy_training(pid):
        """ Returns the points to plot from the training_progress table. """
        results = current_app.config['FE'].ep_input.get_column_by_pid("training_progress", "mse", pid )
        return results

    @bp.route("/processes")
    @login_required
    def process_index():
        """Show the processes index."""
        process_list = current_app.config['FE'].ep_input.get_processes(
            current_user.id)
        return render_template("/process/index.html", process_list=process_list)

    @bp.route("/process/<pid>")
    @login_required
    def process_detail(pid):
        """Show the process detail view, if it is the current user, shows a change password button."""
        process_list = current_app.config['FE'].ep_input.get_process_by_pid(pid)
        return render_template("/process/detail.html", process_list = process_list, pid = pid)

    @bp.route("/dashboard/configs")
    #@login_required
    def configs_index():
        """Show the processes index."""
        p_config = load_plugin_config()
        p_config_gui = p_config["gui"]
        return render_template("/configs/index.html", p_config=p_config_gui)

    return bp