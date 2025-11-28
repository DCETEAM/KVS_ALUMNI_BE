import logging
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
import os

db = SQLAlchemy()

def create_app():

    logging.basicConfig(
        level=logging.DEBUG, 
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    app = Flask(__name__)
    CORS(app)

    # Load config
    try:
        app.config.from_object(Config)
        logging.info("Configuration loaded successfully.")
    except Exception as e:
        logging.error(f"Configuration failed: {e}")

    # Init DB
    try:
        db.init_app(app)
        logging.info("DB initialized successfully.")
    except Exception as e:
        logging.error(f"DB initialization failed: {e}")

    Migrate(app, db)
    logging.info("Migrate initialized successfully.")

    # -----------------------------------------
    #   STATIC FILE ROUTES
    # -----------------------------------------

    @app.route('/register/profile/<filename>')
    def serve_profile(filename):
        """Serve profile images stored in src/assets"""
        upload_path = os.path.join(app.root_path, "assets")
        return send_from_directory(upload_path, filename)

    @app.route('/register/profile/qr/<filename>')
    def serve_qr(filename):
        qr_path = os.path.join(app.root_path, "assets", "qrcodes")
        print("Serving QR from:", qr_path)
        return send_from_directory(qr_path, filename)


    # -----------------------------------------
    #   ROUTES
    # -----------------------------------------
    try:
        from src.routes import init_routes
        init_routes(app)
        logging.info("Routes initialized successfully.")
    except Exception as e:
        logging.error(f"Route init error: {e}")

    # Create tables
    with app.app_context():
        db.create_all()

    return app
