# -*- encoding: utf-8 -*-
from flask import Blueprint, jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from app.app import db, login_manager
from .forms import LoginForm, CreateAccountForm
from app.util import verify_pass

def new_bp(plugin_folder, core_ep, store_ep):
    
    bp = Blueprint("base_bp", __name__, url_prefix='', template_folder=plugin_folder+"/templates", static_folder=plugin_folder+"/static")
    User = core_ep.User

    ## Login & Registration
    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        login_form = LoginForm(request.form)
        if 'login' in request.form:
            # read form data
            username = request.form['username']
            password = request.form['password']
            # Locate user
            user = User.query.filter_by(username=username).first()
            # Check the password
            if user and verify_pass( password, user.password):

                login_user(user)
                return redirect('/')

            # Something (user or pass) is not ok
            return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

        if not current_user.is_authenticated:
            return render_template( 'accounts/login.html',
                                    form=login_form)
        #return redirect(url_for('data_logger.index'))
        return redirect(url_for('home_bp.index'))

    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        login_form = LoginForm(request.form)
        create_account_form = CreateAccountForm(request.form)
        if 'register' in request.form:

            username  = request.form['username']
            email     = request.form['email'   ]

            # Check usename exists
            user = User.query.filter_by(username=username).first()
            if user:
                return render_template( 'accounts/register.html', 
                                        msg='Username already registered',
                                        success=False,
                                        form=create_account_form)

            # Check email exists
            user = User.query.filter_by(email=email).first()
            if user:
                return render_template( 'accounts/register.html', 
                                        msg='Email already registered', 
                                        success=False,
                                        form=create_account_form)

            # else we can create the user
            user = User(**request.form)
            db.session.add(user)
            db.session.commit()

            return render_template( 'accounts/register.html', 
                                    msg='User created please <a href="/login">login</a>', 
                                    success=True,
                                    form=create_account_form)

        else:
            return render_template( 'accounts/register.html', form=create_account_form)

    @bp.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('base_bp.login'))

    @bp.route('/shutdown')
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return 'Server shutting down...'

    ## Errors

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return render_template('page-403.html'), 403

    @bp.errorhandler(403)
    def access_forbidden(error):
        return render_template('page-403.html'), 403

    @bp.errorhandler(404)
    def not_found_error(error):
        return render_template('page-404.html'), 404

    @bp.errorhandler(500)
    def internal_error(error):
        return render_template('page-500.html'), 500

    return bp