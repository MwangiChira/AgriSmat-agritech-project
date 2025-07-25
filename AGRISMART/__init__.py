# app/__init__.py

from flask import Flask
from .routes import main_bp

def create_app():
    """Application factory: creates and configures the Flask app."""
    app = Flask(__name__, instance_relative_config=True)
    # Load default config (can override in instance/config.py)
    app.config.from_object('config.Config')
    # Optionally load instance config (for SECRET_KEY, etc.)
    try:
        app.config.from_pyfile('config.py')
    except FileNotFoundError:
        pass

    # Register Blueprints
    app.register_blueprint(main_bp)

    return app
