from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase

# Create a base class for our models
class Base(DeclarativeBase):
    pass

# Initialize extensions (without binding to app yet)
db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
