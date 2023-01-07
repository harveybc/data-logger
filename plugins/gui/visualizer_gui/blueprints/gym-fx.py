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

def new_bp(plugin_folder, core_ep, store_ep, db, Base):

    # construct the gym-fx blueprint using the plugin folder as template folder
    bp = Blueprint("gym_fx_bp", __name__,
                   template_folder=plugin_folder+"/templates")

    # create the blueprint for the post and get methods
    @bp.route("/gym-fx/<config_id>", methods=['POST', 'GET'])
    @login_required
    def gym_fx(config_id):
        if request.method == 'POST':
            """ Creates a new register using Automap Base. """
            # create new register
            try:
                with app.app_context():
                    gym_fx_class = Base.classes.gy m_fx
                    new_reg = gym_fx_class()
                    new_reg.score = request.form['score_v']
                    new_reg.avg_score_v = request.form['avg_score_v']
                    new_reg.score_v = request.form[' training_score']
                    new_reg.avg_score = request.form['avg_score']
                    info = json.loads(request.form['info' ])
                    new_reg.reward = info['reward']
                    new_reg.balance = info['balance']
                    new_reg.equity = info['equity']
                    new_reg.margin = info['margin']
                    new_reg.config_id = config_id
                    db = get_db()
                    error = None
                    db.session.add(new_reg)
            except SQLAlchemyError as e:
                error = str(e)
                print("Error : ", error)
                res = {'error_ca': error}
            attr = getattr(res, "config_id")
            return str(attr)
    return bp
