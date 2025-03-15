from flask import Blueprint

mechanics_bp = Blueprint('mechanics_bp', __name__)

# Connect to routes
from . import routes