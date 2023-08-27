# this file contains the blueprint for the gym-fx data_logger process

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
from sqlalchemy import  asc, desc
from sqlalchemy.sql.expression  import func
import json
from sqlalchemy.orm import Session
from sqlalchemy import inspect


def new_bp(plugin_folder, core_ep, store_ep, db, Base):

    # construct the gym-fx blueprint using the plugin folder as template folder
    bp = Blueprint("gym_fx_bp", __name__,
                   template_folder=plugin_folder+"/templates")
    database = db
    # create the blueprint for the post and get methods
    @bp.route("/gym-fx/<config_id>", methods=['POST', 'GET'])
    @login_required
    def gym_fx(config_id):
        if request.method == 'POST':
            """ Creates a new register using Automap Base. """
            # create new register
            try:
                gym_fx_class = Base.classes.gym_fx_data
                new_reg = gym_fx_class()
                session = Session(database.engine)
                data = request.json
                new_reg.score = data['score']                
                new_reg.avg_score = data['avg_score']
                new_reg.score_v = data['score_v']
                new_reg.avg_score_v = data['avg_score_v']
                info = data['info']
                new_reg.reward = info['reward']
                new_reg.balance = info['balance']
                new_reg.equity = info['equity']
                new_reg.margin = info['margin']
                new_reg.config_id = config_id
                db = get_db()
                error = None
                session.add(new_reg)
                session.commit()
            except SQLAlchemyError as e:
                error = str(e)
                print("Error : ", error)
                new_reg = error
                return new_reg
            return as_dict(new_reg)
    
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
            print("Error : " , error)
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
            print("Error : " , error)
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
            error = str(e)
            print("Error : " , error)
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
            print("Error : " , error)
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
            print("Error : " , error)
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
            best = int(gymfx_best_offline_())
            print("best_offline : " , best)
            points = db.session.query(Base.classes.gym_fx_validation_plot).filter(Base.classes.gym_fx_validation_plot.config_id == best ).order_by(asc(Base.classes.gym_fx_validation_plot.id)).limit(num_points).all()
            res = list(map(as_dict, points))
        except Exception as e:
            error = str(e)
            print("Error : " , error)
            return error
        return json.dumps(res)
    
    def row2dict(obj):
        return {
            c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs
        }

    @bp.route('/gymfx_process_list_')
    @login_required
    def gymfx_process_list_():
        """ TODO: Returns a list of processes in the gym_fx_data that has config.active == true. """
        # table base class
        #Base.prepare(db.engine)
        # perform query, the column classs names are configured in config_store.json
        try:
            # query for the different gym_fx_config.id and max validation score where gym_fx_config.active == True
            res = db.session.query(Base.classes.gym_fx_config, func.max(Base.classes.gym_fx_data.score_v).label("max"))\
                .join(Base.classes.gym_fx_data, (Base.classes.gym_fx_data.config_id == Base.classes.gym_fx_config.id))\
                .filter(Base.classes.gym_fx_config.active == True).group_by(Base.classes.gym_fx_data.config_id).all()             
        except SQLAlchemyError as e:
            error = str(e)
            print("SQLAlchemyError : " , error)
            return error
        except Exception as e:
            error = str(e)
            print("Error : " , error)
            return error
        res_list = []
        for r in res:
            res_list.append(r.max)
        return json.dumps(res_list)

    return bp
