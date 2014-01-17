# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, session, jsonify)
from sqlalchemy.exc import IntegrityError

from fpage.models import User, Submission
from fpage.forms import RegisterForm, LoginForm
from fpage.utils import flash_errors, login_required
from fpage.models import db

blueprint = Blueprint('public', __name__,
                        static_folder="../static",
                        template_folder="../templates")


@blueprint.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", posts=Submission.query.order_by(Submission.ups))


@blueprint.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['username']).first()
        if u is None or not u.check_password(request.form['password']):
            error = 'Invalid username or password.'
            flash(error, 'warning')
        else:
            session['logged_in'] = True
            session['username'] = u.username
            flash("You are logged in.", 'success')
            return redirect(url_for("public.home"))
    return render_template("login.html", form=form)


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User(form.username.data, form.email.data, form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Thank you for registering. You can now log in.", 'success')
            return redirect(url_for('public.home'))
        except IntegrityError as err:
            flash("That username and/or email already exists. Try again.", 'warning')
    else:
        flash_errors(form)
    return render_template('register.html', form=form)

@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("about.html", form=form)

@blueprint.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

    # @blueprint.route('/translate', methods = ['POST'])
    # @login_required
    # def translate():
    #     print "translating"
    #     return jsonify({
    #         'text': "100"})