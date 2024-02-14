
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
from app.util import load_plugin_config

def new_bp(plugin_folder, core_ep, store_ep, db, Base):

    # construct the data_logger blueprint using the plugin folder as template folder
    bp = Blueprint("dashboard_bp", __name__, template_folder=plugin_folder+"/templates")
    # load current store and gui plugins
    p_config = load_plugin_config()            
    p_config_gui = p_config["gui"]
    p_config_store = p_config["store"]
    
    @bp.route("/")
    #@login_required
    def index():
        box= []
        status = []
        p_config = load_plugin_config()
        return render_template("/dashboard/index.html", p_config_gui = p_config["gui"], p_config_store = p_config["store"])
    
    # returns the config id for the best score from table gym_fx_data that has config.active == true
    @bp.route('/gymfx_best_online_')
    @login_required
    def gymfx_best_online_():
        """ Returns the config id for the best score from table gym_fx_data that has config.active == true. """
        # table base class
        #Base.prepare(db.engine)
        # perform query, the column classs names are configured in config_store.json
        try:
            # query for the maximum score from the gym_fx_data table for the config_id whose gymfx_config.active == True
            res = db.session.query(Base.classes.gym_fx_data).join(Base.classes.gym_fx_config, Base.classes.gym_fx_data.config_id == Base.classes.gym_fx_config.id).filter(Base.classes.gym_fx_config.active == True).order_by(desc(Base.classes.gym_fx_data.score)).first_or_404()
        except SQLAlchemyError as e:
            error = str(e)
            print("SQLAlchemyError : " , error)
            return error
        except Exception as e:
            error = str(e)
            print("Error : " ,error)
            return error
        attr = getattr(res, "config_id")
        return json.dumps(attr)
    
    @bp.route("/gymfx_max_training_score_")
    @login_required
    def gymfx_max_training_score_():
        """ Returns the best score from table gym_fx_data that has config.active == true. """
        # table base class
        #Base.prepare(db.engine)
        # perform query, the column classs names are configured in config_store.json
        try:
            res = db.session.query(Base.classes.gym_fx_data).join(Base.classes.gym_fx_config, Base.classes.gym_fx_data.config_id == Base.classes.gym_fx_config.id).filter(Base.classes.gym_fx_config.active == True).order_by(desc(Base.classes.gym_fx_data.score)).first_or_404()
        except Exception as e:
            error = str(e)
            print("Error : " ,error_f(error))
            return error
        attr = getattr(res, "score")
        return json.dumps(attr)

    @bp.route("/gymfx_best_offline_")
    @login_required
    def gymfx_best_offline_():
        """ Returns the config id for the best score from table gym_fx_data that has config.active == false. """
        # table base class
        #Base.prepare(db.engine)
        # perform query, the column classs names are configured in config_store.json
        try:
            res = db.session.query(Base.classes.gym_fx_data).join(Base.classes.gym_fx_config, Base.classes.gym_fx_data.config_id == Base.classes.gym_fx_config.id).filter(Base.classes.gym_fx_config.active == False).order_by(desc(Base.classes.gym_fx_data.score_v)).first_or_404()
        except Exception as e:
            # TODO: use some form of error management to ease tracing of errors
            error = str(e)
            print("Error : No inactive (finished) registers in gym_fx_config table to search for their validation plot. " ,error_f(error))
            return error
        attr = getattr(res, "config_id")
        return json.dumps(attr)
           
    @bp.route("/gymfx_max_validation_score_")
    @login_required
    def gymfx_max_validation_score_():
        """ Returns the best score_v from table gym_fx_data that has config.active == false. """
        # table base class
        #Base.prepare(db.engine)
        # perform query, the column classs names are configured in config_store.json
        try:
            res = db.session.query(Base.classes.gym_fx_data).join(Base.classes.gym_fx_config, Base.classes.gym_fx_data.config_id == Base.classes.gym_fx_config.id).filter(Base.classes.gym_fx_config.active == False).order_by(desc(Base.classes.gym_fx_data.score_v)).first_or_404()
        except Exception as e:
            error = str(e)
            print("Error : " ,error_f(error))
            return error
        attr = getattr(res, "score")
        return json.dumps(attr)
    
    @bp.route("/gymfx_online_plot_")
    @login_required
    def gymfx_online_plot_():
        """ Returns an array of points [tick_count, score] from the gym_fx_data table for thebest prcess with config_id.active== True. """
        args = request.args
        num_points = args.get("num_points", default=100, type=int)
        
        # perform query, the column classs names are configured in config_store.json
        try:
            best = int(gymfx_best_online_())
            print("best : " , best)
            points = db.session.query(Base.classes.gym_fx_data).filter(Base.classes.gym_fx_data.config_id == best ).order_by(desc(Base.classes.gym_fx_data.id)).limit(num_points).all()
            res = []
            count = 0
            for p in points:
                res.append({"x":count, "y":p.score})
                count += 1
        except Exception as e:
            error = str(e)
            print("Error : " ,error_f(error))
            return error
        return json.dumps(res)
    
    @bp.route("/gymfx_validation_plot_")
    @login_required
    def gymfx_validation_plot_():
        """ Returns a json with the initial capital and arrays for the columns order_status, tick_date, balance, equity,margin,reward from the gym_fx_data table for thebest prcess with config_id.active== True. """
        args = request.args
        num_points = args.get("num_points", default=1000, type=int)
        # perform query, the column classs names are configured in config_store.json
        try:
            #TODO: verify errror in here
            best = int(gymfx_best_offline_())
            print("best_offline : " , best)
            points = db.session.query(Base.classes.gym_fx_validation_plot).filter(Base.classes.gym_fx_validation_plot.config_id == best ).order_by(asc(Base.classes.gym_fx_validation_plot.id)).limit(num_points).all()
            res = list(map(as_dict, points))
        except Exception as e:
            error = str(e)
            print("Error : " ,error_f(error))
            return error
        return json.dumps(res)
    
    @bp.route('/gymfx_process_list_')
    @login_required
    def gymfx_process_list_():
        """ TODO: Returns a list of processes in the gym_fx_data that has config.active == true. """
        # table base class
        #Base.prepare(db.engine)
        # perform query, the column classs names are configured in config_store.json
        try:
            # query for the different gym_fx_config.id and max validation score where gym_fx_config.active == True
            res = db.session.query(Base.classes.gym_fx_config.id.label("id"), Base.classes.gym_fx_config.active.label("active"), func.max(Base.classes.gym_fx_data.score_v).label("max"))\
                .join(Base.classes.gym_fx_data, (Base.classes.gym_fx_data.config_id == Base.classes.gym_fx_config.id))\
                .group_by(Base.classes.gym_fx_data.config_id).all()             
        except SQLAlchemyError as e:
            error = str(e)
            print("SQLAlchemyError : " , error)
            return error
        except Exception as e:
            error = str(e)
            print("Error : " ,error_f(error))
            return error
        res_list = []
        for r in res:
            res_list.append({'id':r.id, 'max': r.max, 'active': r.active})
        return json.dumps(res_list)

    return bp