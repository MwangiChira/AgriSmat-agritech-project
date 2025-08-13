# app/__init__.py

import os
from flask import Flask
from .routes import main_bp

def create_app():
    """Application factory: creates and configures the Flask app."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Load default config
    try:
        app.config.from_object('config.Config')
    except ImportError:
        pass
    
    # Optionally load instance config (for SECRET_KEY, etc.)
    try:
        app.config.from_pyfile('config.py')
    except FileNotFoundError:
        pass

    # Register Blueprints
    app.register_blueprint(main_bp)

    return app