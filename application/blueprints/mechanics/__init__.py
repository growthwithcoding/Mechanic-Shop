# application/blueprints/mechanics/__init__.py
from flask import Blueprint
mechanics_bp = Blueprint("mechanics", __name__)
from . import routes  # <-- this line ensures routes are registered
