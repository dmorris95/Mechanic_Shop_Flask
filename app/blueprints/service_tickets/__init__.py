from flask import Blueprint

tickets_bp = Blueprint('tickets_bp', __name__)

# Connect to routes
from . import routes