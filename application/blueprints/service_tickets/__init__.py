# application/blueprints/service_tickets/__init__.py
from flask import Blueprint
service_tickets_bp = Blueprint("service_tickets", __name__)
from . import routes  # <-- this line ensures routes are registered
