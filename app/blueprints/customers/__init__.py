from flask import Blueprint

customers_bp = Blueprint('customers_bp', __name__)

# Connect with routes
from . import routes