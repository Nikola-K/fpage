# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template
# from flask_debugtoolbar import DebugToolbar

from fpage.settings import ProdConfig
from fpage.assets import assets
from fpage.extensions import (db, login_manager, migrate, cache)
from fpage import public, user, comment, submission, votes, admin, message


def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    assets.init_app(app)
    # toolbar = DebugToolbarExtension(app)
    cache.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(comment.views.blueprint)
    app.register_blueprint(submission.views.blueprint)
    app.register_blueprint(votes.views.blueprint)
    app.register_blueprint(admin.views.blueprint)
    app.register_blueprint(message.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        return render_template("{0}.html".format(error.code)), error.code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None