from flask import Flask
import os

from infrastructure.ir_cache import IRCache
from utilities.file_handling import load_ir

from services.dashboard_service import DashboardService
from services.explorer_service import ExplorerService
from services.trace_service import TraceService


def ensure_directories():
    os.makedirs("data", exist_ok=True)


def create_app():
    ensure_directories()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key'

    # -----------------------------------
    # Infrastructure layer
    # -----------------------------------
    ir_cache = IRCache(load_ir)

    # -----------------------------------
    # Service layer
    # -----------------------------------
    dashboard_service = DashboardService(ir_cache)
    explorer_service = ExplorerService(ir_cache)
    trace_service = TraceService(ir_cache)

    # -----------------------------------
    # API layer (Blueprints)
    # -----------------------------------
    from api.index_routes import index_bp
    from api.dashboard_routes import dashboard_bp
    from api.trace_routes import trace_bp
    from api.explorer_routes import explorer_bp

    # Inject services into blueprints
    dashboard_bp.dashboard_service = dashboard_service
    explorer_bp.explorer_service = explorer_service
    trace_bp.trace_service = trace_service

    # Register blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(trace_bp)
    app.register_blueprint(explorer_bp)

    return app
