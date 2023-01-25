
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
        p_config_gui = p_config["gui"]
        return render_template("/dashboard/index.html", p_config = p_config_gui)

    # returns the config id for the best mse from table gym_fx_data that has config.active == true
    @bp.route('/gymfxbestonline')
    @login_required
    def gymfx_best_online_():
        """ Returns the config id for the best mse from table gym_fx_data that has config.active == true. """
        # table base class
        #Base.prepare(db.engine)
        # perform query, the column classs names are configured in config_store.json
        try:
            # query for the maximum reward from the gym_fx_data table for the config_id whose gymfx_config.active == True
            res = db.session.query(Base.classes.gym_fx_data).join(Base.classes.gym_fx_config, Base.classes.gym_fx_data.config_id == Base.classes.gym_fx_config.id).filter(Base.classes.gym_fx_config.active == True).order_by(desc(Base.classes.gym_fx_data.score)).first_or_404()
        except SQLAlchemyError as e:
            error = str(e)
            print("SQLAlchemyError : " , error)
            return error
        except Exception as e:
            error = str(e)
            print("Error : " , error)
            return error
        attr = getattr(res, "config_id")
        return str(attr)
    
    @bp.route("/gymfx_max_training_score_")
    @login_required
    def gymfx_max_training_score_():
        """ Returns the best mse from table gym_fx_data that has config.active == true. """
        # table base class
        #Base.prepare(db.engine)
        # perform query, the column classs names are configured in config_store.json
        try:
            res = db.session.query(Base.classes.gym_fx_data).join(Base.classes.gym_fx_config, Base.classes.gym_fx_data.config_id == Base.classes.gym_fx_config.id).filter(Base.classes.gym_fx_config.active == True).order_by(desc(Base.classes.gym_fx_data.score)).first_or_404()
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            res = { 'error_ca' : error}
        attr = getattr(res, "mse")
        return str(attr)

    @bp.route("/gymfx_best_config_")
    @login_required
    def gymfx_best_config_():
        """ Returns the config id for the best mse from table gym_fx_data that has config.active == false. """
        # table base class
        #Base.prepare(db.engine)
        # perform query, the column classs names are configured in config_store.json
        try:
            res = db.session.query(Base.classes.gym_fx_data).join(Base.classes.gym_fx_config, Base.classes.gym_fx_data.config_id == Base.classes.gym_fx_config.id).filter(Base.classes.gym_fx_config.active == False).order_by(desc(Base.classes.gym_fx_data.score_v)).first_or_404()
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            res = { 'error_ca' : error}
        attr = getattr(res, "config_id")
        return str(attr)
           
    @bp.route("/gymfx_max_validation_score_")
    @login_required
    def gymfx_max_validation_score_():
        """ Returns the best mse from table gym_fx_data that has config.active == false. """
        # table base class
        #Base.prepare(db.engine)
        # perform query, the column classs names are configured in config_store.json
        try:
            res = db.session.query(Base.classes.gym_fx_data).join(Base.classes.gym_fx_config, Base.classes.gym_fx_data.config_id == Base.classes.gym_fx_config.id).filter(Base.classes.gym_fx_config.active == False).order_by(desc(Base.classes.gym_fx_data.score_v)).first_or_404()
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            res = { 'error_ca' : error}
        attr = getattr(res, "mse")
        return str(attr)
    
    @bp.route("/online_mse_list")
    @login_required
    def online_mse_list():
        """ Returns the best mse from table gym_fx_data that has config.active == true. """
        # table base class
        #Base.prepare(db.engine)
        # perform query, the column classs names are configured in config_store.json
        try:
            res = db.session.query(Base.classes.gym_fx_data).join(Base.classes.gym_fx_config, Base.classes.gym_fx_data.config_id == Base.classes.gym_fx_config.id).filter(Base.classes.gym_fx_config.active == True).order_by(asc(Base.classes.gym_fx_data.mse)).first_or_404()
            best_online_config = getattr(res, "config_id")
            res = db.session.query(Base.classes.gym_fx_data).filter(Base.classes.gym_fx_data.config_id == best_online_config).order_by(desc(Base.classes.gym_fx_data.timestamp)).limit(10).all()
            # convert to list of lists of timestamp and mse
            res = [[row.timestamp, row.mse] for row in res]
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            res = { 'error_ca' : error}        
        return json.dumps(res)
    
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