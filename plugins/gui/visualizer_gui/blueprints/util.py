
# This file contains the util requests used by the gui

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
    bp = Blueprint("util_bp", __name__, template_folder=plugin_folder+"/templates")
    
    @bp.route("/user_column_max")
    #@login_required
    def column_max():
        table = request.args.get('table')
        column = request.args.get('column')
        if ((not table) or (not column)):
            abort(500, "Either table:{table} or column:{column} are null.")
        results = core_ep.column_max(db, table, column)
        return results

#    @bp.route("/<int:pid>/trainingpoints")
#    def get_points(pid):
#        """Get the points to plot from the training_progress table and return them as JSON."""
#        xy_points = get_xy_training(pid)
#        return jsonify(xy_points)
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