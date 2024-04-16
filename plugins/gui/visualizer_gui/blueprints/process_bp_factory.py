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
from app.util import load_plugin_config, sanitize_str
from .process_tables.read import read_data
from .process_tables.index import list_data, scoreboard_data, online_plot_data, static_plot_data
import json


def ProcessBPFactory(process, table):
    def new_bp(plugin_folder, core_ep, store_ep, db, Base):
        # construct the blueprint using the process ant table parameters of the factory
        bp = Blueprint("bp_"+process["name"]+"_"+table["name"], __name__, template_folder=plugin_folder+"/templates")
        # read gui plugin config and endpoint routes for CRUD
        p_config = load_plugin_config()            
       
        # endpoint View Create
        @bp.route("/"+process["name"]+"/"+table["name"]+"/view_create")
        def view_create():
            return render_template("/process_tables/create.html", p_config_gui = p_config["gui"], p_config_store = p_config["store"], process=process, table=table)
        
        # endpoint View Detail
        @bp.route("/"+process["name"]+"/"+table["name"]+"/view_detail/<id>")
        def view_detail(id):
            return render_template("/process_tables/read.html", id=id, p_config_gui = p_config["gui"], p_config_store = p_config["store"], process=process, table=table)
        
        # endpoint View Update
        @bp.route("/"+process["name"]+"/"+table["name"]+"/view_edit/<id>")
        def view_edit(id):
            return render_template("/process_tables/edit.html", id=id, p_config_gui = p_config["gui"], p_config_store = p_config["store"], process=process, table=table)
        
        # endpoint View Remove
        @bp.route("/"+process["name"]+"/"+table["name"]+"/view_remove/<id>")
        def view_remove(id):
            return render_template("/process_tables/remove.html", id=id, p_config_gui = p_config["gui"], p_config_store = p_config["store"], process=process, table=table)
        
        # endpoint View Index
        @bp.route("/"+process["name"]+"/"+table["name"]+"/view_index")
        def view_index():
            args = request.args
            page_num = args.get("page_num", default=1, type=int)
            num_rows = args.get("num_rows", default=15, type=int)
            num_points = args.get("num_points", default=100, type=int)
            return render_template("/process_tables/index.html", p_config_gui = p_config["gui"], p_config_store = p_config["store"], process=process, table=table, page_num=page_num, num_rows=num_rows, num_points=num_points)
        
        # endpoint Index Data
        @bp.route("/"+process["name"]+"/"+table["name"]+"/index_list_data")
        def index_data():
            args = request.args
            page_num = args.get("page_num", default=1, type=int)
            num_rows = args.get("num_rows", default=15, type=int)
            return list_data(db, Base, process, table, page_num, num_rows)
        
        # endpoint create
        @bp.route("/"+process["name"]+"/"+table["name"]+"/create", methods=("POST",))
        def create():
            """Create a new register for the table"""
            try:
                print("Request form: ", request.form)
                body = request.form.to_dict(flat=True)
                print("Body: ", body)
                reg_model = Base.classes[table['name']]
                reg = reg_model(**body)
                db.session.add(reg)
                db.session.commit()
                return jsonify({ "result": "ok" })
            except Exception as e:
                error = str(e)
                print("Error : " ,error)
                abort(500)
        
        # endpoint detail
        @bp.route("/"+process["name"]+"/"+table["name"]+"/detail/<id>")
        def detail(id):
            return read_data(db, Base, process, table, id)
        
        # endpoint update
        @bp.route("/"+process["name"]+"/"+table["name"]+"/edit", methods=("POST",))
        def edit():
            """Update a register for the table"""
            body = request.json
            reg_model = core_ep.ProcessRegisterFactory(table["name"], Base)
            res = reg_model.update(**body)
            return jsonify(res)

        # endpoint remove
        @bp.route("/"+process["name"]+"/"+table["name"]+"/remove/<id>", methods=("POST",))
        def remove(id):
            """Remove a register for the table"""
            reg_model = core_ep.ProcessRegisterFactory(table["name"], Base)
            res = reg_model.delete(id)
            return jsonify(res)

        # returns the config id for the best score from table gym_fx_data that has config.active == true
        @bp.route("/"+process["name"]+"/"+table["name"]+"/scoreboard")
        @login_required
        def scoreboard():
            args = request.args
            col = sanitize_str(args.get("col", default="config_id", type=str), 256)
            order_by = sanitize_str(args.get("order_by", default="score", type=str), 256)
            order = sanitize_str(args.get("order", default="desc", type=str), 256)
            foreign_key = sanitize_str(args.get("foreign_key", default="config_id", type=str), 256)
            rel_table = sanitize_str(args.get("rel_table", default="gym_fx_config", type=str), 256)
            rel_filter_col = sanitize_str(args.get("rel_filter_col", default="active", type=str), 256)
            rel_filter_op = sanitize_str(args.get("rel_filter_op", default="is_equal", type=str), 256)
            rel_filter_val = sanitize_str(args.get("rel_filter_val", default=True), 256)
            if rel_filter_val == "True":
                rel_filter_val = True
            if rel_filter_val == "False":
                rel_filter_val = False
            # return scoreboard_data(db, Base, process, table, page_num, num_rows)
            return scoreboard_data(db, Base, table["name"], col, order_by, order, foreign_key, rel_table, rel_filter_col, rel_filter_op, rel_filter_val)

        @bp.route("/"+process["name"]+"/"+table["name"]+"/online_plot")
        @login_required
        def online_plot():
            args = request.args
            num_points = args.get("num_points", default=100, type=int)

            val_col = sanitize_str(args.get("val_col", default="config_id", type=str), 256)
            best_col = sanitize_str(args.get("best_col", default="score", type=str), 256)
            order_by = sanitize_str(args.get("order_by", default="score", type=str), 256)
            order = sanitize_str(args.get("order", default="desc", type=str), 256)
            foreign_key = sanitize_str(args.get("foreign_key", default="config_id", type=str), 256)
            rel_table = sanitize_str(args.get("rel_table", default="gym_fx_config", type=str), 256)
            rel_filter_col = sanitize_str(args.get("rel_filter_col", default="active", type=str), 256)
            rel_filter_op = sanitize_str(args.get("rel_filter_op", default="is_equal", type=str), 256)
            rel_filter_val = sanitize_str(args.get("rel_filter_val", default=True), 256)
            if rel_filter_val == "True":
                rel_filter_val = True
            if rel_filter_val == "False":
                rel_filter_val = False
            # return online_plot_data(db, Base, process, table, page_num, num_rows)
            return online_plot_data(db, Base, num_points, table["name"], val_col, best_col, order_by, order, foreign_key, rel_table, rel_filter_col, rel_filter_op, rel_filter_val)

        @bp.route("/"+process["name"]+"/"+table["name"]+"/static_plot")
        @login_required
        def static_plot():
            args = request.args
            num_points = args.get("num_points", default=100, type=int)

            val_col = sanitize_str(args.get("val_col", default="config_id", type=str), 256)
            best_col = sanitize_str(args.get("best_col", default="score", type=str), 256)
            order_by = sanitize_str(args.get("order_by", default="score", type=str), 256)
            order = sanitize_str(args.get("order", default="desc", type=str), 256)
            foreign_key = sanitize_str(args.get("foreign_key", default="config_id", type=str), 256)
            rel_table = sanitize_str(args.get("rel_table", default="gym_fx_config", type=str), 256)
            rel_filter_col = sanitize_str(args.get("rel_filter_col", default="active", type=str), 256)
            rel_filter_op = sanitize_str(args.get("rel_filter_op", default="is_equal", type=str), 256)
            rel_filter_val = sanitize_str(args.get("rel_filter_val", default=True), 256)
            if rel_filter_val == "True":
                rel_filter_val = True
            if rel_filter_val == "False":
                rel_filter_val = False
            # return online_plot_data(db, Base, process, table, page_num, num_rows)
            return static_plot_data(db, Base, num_points, table["name"], val_col, best_col, order_by, order, foreign_key, rel_table, rel_filter_col, rel_filter_op, rel_filter_val)
 

        return bp
    return new_bp
