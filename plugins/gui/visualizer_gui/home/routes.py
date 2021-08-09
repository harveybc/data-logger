# -*- encoding: utf-8 -*-


from ..home import blueprint
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.app import login_manager
from jinja2 import TemplateNotFound

#TOD: Importar authorization required desde core_ep.


#from ..controllers.authorization import authorization_required

@blueprint.route('/index')
#@authorization_required
def index():

    return render_template('index.html')

@blueprint.route('/<template>')
#@authorization_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        return render_template( template )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500
