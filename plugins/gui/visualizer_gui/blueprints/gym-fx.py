
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
        	gym_fx_class = Base.classes.gym_fx
            new_reg = gym-fx()
            new_reg.validation_score = request.form['validation_score']
            new_reg.avg_score_v = request.form['avg_score_v']
            new_reg.training_score = request.form[' training_score']
            new_reg.avg_score = request.form['avg_score']
            info = request.form['info' ]
            db = get_db()
            error = None
        # perform query, the column classs names are configured in config_store.json
        try:
            # res = db.session.query(func.min(Base.classes.fe_training_error.mse)).filter_by('some name', id = 5)
            #res = db.session.query(Base.classes.gym_fx).join(Base.classes.gym_fx_config, Base.classes.fe_training_error.config_id == Base.classes.fe_config.id).filter(
                Base.classes.fe_config.active == True).order_by(asc(Base.classes.fe_training_error.mse)).first_or_404()
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : ", error)
            res = {'error_ca': error}
        attr = getattr(res, "config_id")

        return str(attr)
    return bp
