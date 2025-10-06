"""
config.py - Centralized configuration for Application Factory
"""
import os

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("APP_DATABASE_URI", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True

class TestingConfig(BaseConfig):
    ENV = "testing"
    TESTING = True
    DEBUG = True

class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = False

CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
