from flask import Blueprint, render_template, jsonify, request
from utilities.file_handling import open_json
'''from services.trace_service import get_trace'''


trace_bp = Blueprint('trace', __name__, url_prefix='/trace')
'''
Endpoints:
GET /trace/<project>/triggers
GET /trace/<project>/run
GET /trace/<project>/mermaid
'''



