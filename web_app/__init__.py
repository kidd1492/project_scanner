from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key'

    # Import blueprints from the api package
    from api.project_routes import project_bp


    # Register blueprints
    app.register_blueprint(project_bp)
    return app
