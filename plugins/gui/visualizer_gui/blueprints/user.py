
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
from flask import request

def new_bp(plugin_folder, core_ep):

    # construct the data_logger blueprint using the plugin folder as template folder
    bp = Blueprint("user_bp", __name__, template_folder=plugin_folder+"/templates")

    @bp.route("/views/users")
    #@login_required
    def user_index():
        """Show the users index."""
        user_list = core_ep.User.real_all()
        return render_template("../"/"user/index.html", user_list = user_list)

    @bp.route("/views/user/create", methods=["GET"])
    @login_required
    def user_create_view():
        """Show the users index."""
        return render_template("../"/"user/create.html")
    
    @bp.route("/views/user/create", methods=["POST"])
    @login_required
    def user_create():
        """Show the users index."""
        result = current_app.config['FE'].ep_input.user_create(request.form)
        return render_template("../"/"user/create.html")

    @bp.route("/views/user/<username>")
    @login_required
    def user_detail(username):
        """Show the user detail view, if it is the current user, shows a change password button."""
        user_list = current_app.config['FE'].ep_input.get_user_by_username(username)
        return render_template("../"/"user/detail.html", user_list =  user_list, username = username)

    @bp.route("/views/user/<int:id>/update", methods=("GET", "POST"))
    @login_required
    def update(id):
        """Update a post if the current user is the author."""
        post = get_post(id)
        if request.method == "POST":
            title = request.form["title"]
            body = request.form["body"]
            error = None
            if not title:
                error = "Title is required."
            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute(
                    "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
                )
                db.commit()
                return redirect(url_for("data_logger.index"))
        return render_template("data_logger/update.html", post=post)

    @bp.route("/views/user/<int:id>/delete", methods=("POST",))
    @login_required
    def delete(id):
        """Delete a post.

        Ensures that the post exists and that the logged in user is the
        author of the post.
        """
        get_post(id)
        db = get_db()
        db.execute("DELETE FROM post WHERE id = ?", (id,))
        db.commit()
        return redirect(url_for("data_logger.index"))    
 
    return bp
