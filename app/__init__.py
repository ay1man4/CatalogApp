import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()


def create_app(config_name):
    if config_name is None:
        config_name = 'development'
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_pyfile('config.py')

    db.init_app(app)

    migrate = Migrate(app, db)

    from app.auth.views import auth
    app.register_blueprint(auth)

    from app.home.views import home
    app.register_blueprint(home)

    from app.api.views import api
    app.register_blueprint(api)

    # Create DB tables
    @app.before_first_request
    def create_tables():
        db.create_all()

    # Handling errors
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    return app
