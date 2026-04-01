from flask import Blueprint, render_template, jsonify

trace_bp = Blueprint('trace', __name__, url_prefix='/trace')