from flask import Flask
from app.adapters.database import db
from app.routes import main
from app.models import CentrifugalPump, Brand
import os
import logging

def create_app():
    app = Flask(__name__)

    configure_database(app)

    return app

def configure_database(app):
    logging.info("Database being configured.")

    try:
        postgres_host = os.getenv("POSTGRES_HOST")
        postgres_user = os.getenv("POSTGRES_USER")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        postgres_db = os.getenv("POSTGRES_DB")
        postgres_port = "5432"

        if not all([postgres_host, postgres_user, postgres_password, postgres_db]):
            raise ValueError("Database connection details are missing.")

        database_uri = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
        print(f"db test: {database_uri}")

        if not database_uri:
            raise ValueError("SQLALCHEMY_DATABASE_URI is not set.")

        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

        app.register_blueprint(main)

        with app.app_context():
            db.create_all()
            Brand.populate()
            CentrifugalPump.populate()
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Starting the app without database configuration.")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise