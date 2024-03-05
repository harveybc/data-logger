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
from app.util import load_plugin_config
from .process_tables.index import list_data_index
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
            return render_template("/process_tables/index.html", p_config_gui = p_config["gui"], p_config_store = p_config["store"], process=process, table=table, page_num=page_num)
        
        # endpoint Index Data
        @bp.route("/"+process["name"]+"/"+table["name"]+"/index_list_data")
        def index_data():
            return list_data_index(db, Base, process, table)
        
        # endpoint create
        @bp.route("/"+process["name"]+"/"+table["name"]+"/create", methods=("POST",))
        def create():
            """Create a new register for the table"""
            try:
                body = json.loads(request.json)
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
            reg_model = core_ep.ProcessRegisterFactory(table["name"], Base)
            res = reg_model.read(id)
            return jsonify(res)
        
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

    

        # endpoint read_range
        @bp.route("/"+process["name"]+"/"+table["name"]+"/read_range/<start>/<end>")
        def read_range(start, end):
            reg_model = core_ep.ProcessRegisterFactory(table["name"], Base)
            res = reg_model.read_range(start, end)
            return jsonify(res)            
        
        # endpoint read_last
        @bp.route("/"+process["name"]+"/"+table["name"]+"/read_last/<length>")
        def read_last(length):
            reg_model = core_ep.ProcessRegisterFactory(table["name"], Base)
            res = reg_model.read_last(start, end)
            return jsonify(res)            
        
        return bp
    return new_bp
