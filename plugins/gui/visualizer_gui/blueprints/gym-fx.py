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
from sqlalchemy import func, asc, desc
import json
from sqlalchemy.orm import Session

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
                new_reg.score = request.form['score']                
                new_reg.avg_score = request.form['avg_score']
                new_reg.score_v = request.form['score_v']
                new_reg.avg_score_v = request.form['avg_score_v']
                #info = json.loads(request.form['info' ])
                #info = json.loads(request.form['info'])
                #print("Info : ", info)
                #new_reg.reward = info['reward']
                #new_reg.balance = info['balance']
                #new_reg.equity = info['equity']
                #new_reg.margin = info['margin']
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
    return bp
