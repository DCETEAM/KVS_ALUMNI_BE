import logging
from flask import Flask, current_app, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
import os

# from src.middlewares.agent_check import restrict_user_agents

# Init db
db = SQLAlchemy()


def create_app():

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s"
    )

    # Create app
    app = Flask(__name__)

    # Handling CORS
    CORS(app)

    # Middlewares
    # Agent check
    # restrict_user_agents(app)

    # Configuration
    try:
        app.config.from_object(Config)
        logging.info("Configuration Success")
    except Exception as e:
        logging.error(f"Configuration Failed, {e}")

    # Connect the db to app
    try:
        db.init_app(app)
        logging.info("DB Initialized Successfully.")
    except Exception as e:
        logging.error(f"DB Initialize Failed, {e}")

    # Init migration
    migrate = Migrate(app, db)
    logging.info("Migrate Initialized Successfully.")

    # Import routes
    try:

        @app.route('/register/profile/<filename>')
        def serve_profile(filename):
            upload_path = os.path.join(os.getcwd(), "src", "assets")
            return send_from_directory(upload_path, filename)

        from src.routes import init_routes

        init_routes(app)
        logging.info("Routes Initialized Successfully.")
    except Exception as e:
        logging.error(f"Routes Initialize Failed ,{e}")

    with app.app_context():
        db.create_all()

    return app
