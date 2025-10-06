# application/blueprints/customers/__init__.py
from flask import Blueprint

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

from . import routes
