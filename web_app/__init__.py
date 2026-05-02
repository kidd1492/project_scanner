from flask import Flask
import os

# --- Infrastructure Tools ---
from infrastructure.file_system.file_handling import FileReader
from infrastructure.file_system.file_discovery import FileDiscovery
from infrastructure.cache_system.typed_ir_cache import TypedIRCache
from infrastructure.plotting.plot_tool import PlotTool

# --- Builder Layer ---
from project_domain.project_ir_builer.builder import ProjectIRBuilder
from project_domain.project_ir_builer.analyzer_manager import AnalyzerManager
from project_domain.dashboard_factory.dashboard_builder import DashboardBuilder

# --- Service Layer ---
from project_domain.project_service import ProjectService


def ensure_directories():
    os.makedirs("cache", exist_ok=True)
    os.makedirs("web_app/static/projects", exist_ok=True)


def create_app():
    ensure_directories()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key'

    # -----------------------------------
    # Infrastructure Tools
    # -----------------------------------
    file_discovery = FileDiscovery()
    file_reader = FileReader()
    persistence = TypedIRCache(cache_dir="cache", file_reader=file_reader)
    plot_tool = PlotTool(base_dir="web_app/static/projects")

    # -----------------------------------
    # Builder Layer
    # -----------------------------------
    project_ir_builder = ProjectIRBuilder()
    analyzer_manager = AnalyzerManager(
        open_file_tool=file_reader,
        project_ir_builder=project_ir_builder
    )

    dashboard_builder = DashboardBuilder(plot_tool=plot_tool)

    # -----------------------------------
    # Service Layer
    # -----------------------------------
    project_service = ProjectService(
        discover_files=file_discovery,
        analyzer_manager=analyzer_manager,
        persistance=persistence,
        dashboard_builder=dashboard_builder
    )

    # -----------------------------------
    # API layer (Blueprints)
    # -----------------------------------
    from api.index_routes import index_bp

    index_bp.project_service = project_service

    app.register_blueprint(index_bp)

    return app
