from flask import Flask
from app.adapters.database import db
from app.routes import main
from app.models import CentrifugalPump, Brand
import os

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable SQLAlchemy event system overhead

    db.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        Brand.populate()
        CentrifugalPump.populate()

    return app
