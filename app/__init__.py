from flask import Flask

from app.config import Config
from app.extensions import cors, db, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "cent-mira-api"}

    # Importing models here makes sure SQLAlchemy knows about them
    # before it tries to create database tables.
    from app import models

    @app.cli.command("create-db")
    def create_db():
        # Flask commands run inside an app context, so db.create_all()
        # knows which Flask app and database configuration to use.
        db.create_all()
        print("Database tables created.")

    from app.blueprints.auth import auth_bp
    from app.blueprints.products import products_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(auth_bp)

    return app
