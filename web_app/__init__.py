from flask import Flask
import os


def ensure_directories():
    os.makedirs("data", exist_ok=True)  # ensures directories exists


def create_app():
    ensure_directories()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key'

    # Import blueprints from the api package
    from api.index_routes import index_bp
    from api.dashboard_routes import dashboard_bp
    from api.trace_routes import trace_bp
    from api.explorer_routes import explorer_bp

    # Register blueprints

    app.register_blueprint(index_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(trace_bp)
    app.register_blueprint(explorer_bp) 
    return app
