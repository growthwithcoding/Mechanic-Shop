# application/__init__.py
from __future__ import annotations
import os
from flask import Flask, jsonify

from .extensions import db, ma, limiter, cache
from . import models  # ensure models are imported so tables are known

# 🔽 These imports MUST be at module scope (not inside create_app)
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.customers import customers_bp  # Added for Assignment 7
from .blueprints.inventory import inventory_bp  # Added for Assignment 10

def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("APP_DATABASE_URI")
    if not app.config["SQLALCHEMY_DATABASE_URI"]:
        raise RuntimeError("APP_DATABASE_URI is not set")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if config_name == "testing":
        app.config["TESTING"] = True
        app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    # 🔽 Blueprints MUST be registered inside create_app
    app.register_blueprint(customers_bp, url_prefix="/customers")  # Added for Assignment 7
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")  # Added for Assignment 10

    with app.app_context():
        db.create_all()

    return app
