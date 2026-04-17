from flask import Flask
import os

from infrastructure.typed_ir_cache import TypedIRCache

from services.dashboard_service import DashboardService
from services.explorer_service import ExplorerService
from services.trace_service import TraceService
from services.project_service import ProjectService


def ensure_directories():
    os.makedirs("cache", exist_ok=True)


def create_app():
    ensure_directories()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key'

    # -----------------------------------
    # Infrastructure layer
    # -----------------------------------
    typed_ir_cache = TypedIRCache()
    typed_ir_cache.preload_all()

    # -----------------------------------
    # Service layer (ALL share same cache)
    # -----------------------------------
    project_service = ProjectService(typed_ir_cache)
    dashboard_service = DashboardService(typed_ir_cache)
    explorer_service = ExplorerService(typed_ir_cache)
    trace_service = TraceService(typed_ir_cache)

    # -----------------------------------
    # API layer (Blueprints)
    # -----------------------------------
    from api.index_routes import index_bp
    from api.dashboard_routes import dashboard_bp
    from api.trace_routes import trace_bp
    from api.explorer_routes import explorer_bp

    # Inject services into blueprints
    index_bp.project_service = project_service
    dashboard_bp.project_service = project_service
    explorer_bp.project_service = project_service

    dashboard_bp.dashboard_service = dashboard_service
    explorer_bp.explorer_service = explorer_service
    trace_bp.trace_service = trace_service

    # Register blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(trace_bp)
    app.register_blueprint(explorer_bp)

    return app
