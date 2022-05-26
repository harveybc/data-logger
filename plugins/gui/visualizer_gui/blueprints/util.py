
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

def new_bp(plugin_folder, core_ep):

    # construct the data_logger blueprint using the plugin folder as template folder
    bp = Blueprint("util_bp", __name__, template_folder=plugin_folder+"/templates")
    
    @bp.route("/column_max")
    #@login_required
    def column_max():
        results = current_app.config['FE'].ep_input.column_max("training_progress", "mse", pid )
        return results

    @bp.route("/<int:pid>/trainingpoints")
    def get_points(pid):
        """Get the points to plot from the training_progress table and return them as JSON."""
        xy_points = get_xy_training(pid)
        return jsonify(xy_points)

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