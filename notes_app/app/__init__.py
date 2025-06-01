from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True) # instance_relative_config=True is good practice

    # Configuration
    # Option 1: Load from .flaskenv (via python-dotenv, which Flask CLI does automatically)
    # For DATABASE_URL, it will be picked up by os.environ.get
    # Option 2: Load from a config.py file or instance folder config
    app.config.from_mapping(
        SECRET_KEY='dev', # Should be overridden in production
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(app.instance_path, 'notes_app.db')}"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # Already exists

    db.init_app(app)

    # Register Blueprints
    from . import routes
    app.register_blueprint(routes.main_bp)

    # If you have other blueprints, register them here
    # from . import auth_bp
    # app.register_blueprint(auth_bp)

    return app
