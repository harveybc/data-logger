
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
from sqlalchemy import func, asc
import json

Base = automap_base()

def new_bp(plugin_folder, core_ep, store_ep, db):

    # construct the data_logger blueprint using the plugin folder as template folder
    bp = Blueprint("dashboard_bp", __name__, template_folder=plugin_folder+"/templates")
    
    @bp.route("/")
    #@login_required
    def index():
        # read the data to be visualized using the using the Feature extractor instance, preinitialized in __init__.py with input and output plugins entry points.
        # TODO: replace 0 in vis_data by process_id, obtained as the first process_id belonging to the current user.    
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
        p_config_gui = p_config["gui"]
        return render_template("/dashboard/index.html", p_config = p_config_gui)

    # returns the config id for the best mse from table fe_training_error that has config.active == true
    @bp.route("/best_online")
    @login_required
    def min_training_mse():
        """ Returns the config id for the best mse from table fe_training_error that has config.active == true. """
        # table base class
        Base.prepare(db.engine, reflect=False)
        # perform query, the column classs names are configured in config_store.json
        try:
            # res = db.session.query(func.min(Base.classes.fe_training_error.mse)).filter_by('some name', id = 5) 
            res = db.session.query(Base.classes.fe_training_error).join(Base.classes.fe_config, Base.classes.fe_training_error.config_id == Base.classes.fe_config.id).filter(Base.classes.fe_config.active == True).order_by(asc(Base.classes.fe_training_error.mse)).first()
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            res = { 'error_ca' : error}
        attr = getattr(res, "config_id")
        print(str(attr))
        print(jsonify(str(attr)))
        return jsonify(str(attr))
           
    def get_xy_training(pid):
        """ Returns the points to plot from the training_progress table. """
        results = current_app.config['FE'].ep_input.get_column_by_pid("training_progress", "mse", pid )
        return results

    @bp.route("/processes")
    @login_required
    def process_index():
        """Show the processes index."""
        process_list = current_app.config['FE'].ep_input.get_processes(current_user.id)
        return render_template("/process/index.html", process_list = process_list)

    @bp.route("/process/<pid>")
    @login_required
    def process_detail(pid):
        """Show the process detail view, if it is the current user, shows a change password button."""
        process_list = current_app.config['FE'].ep_input.get_process_by_pid(pid)
        return render_template("/process/detail.html", process_list = process_list, pid = pid)

    def get_post(id, check_author=True):
        """Get a post and its author by id.

        Checks that the id exists and optionally that the current user is
        the author.

        :param id: id of post to get
        :param check_author: require the current user to be the author
        :return: the post with author information
        :raise 404: if a post with the given id doesn't exist
        :raise 403: if the current user isn't the author
        """
        results = (
            get_db()
            .execute(
                "SELECT p.id, title, body, created, author_id, username"
                " FROM post p JOIN user u ON p.author_id = u.id"
                " WHERE p.id = ?",
                (id,),
            )
            .fetchone()
        )
        # verify if the query returned no results
        if results is None:
            abort(404, "Post id {id} doesn't exist.")
        return results

    return bp