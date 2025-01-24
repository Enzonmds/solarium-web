from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Cargar configuración desde .env
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar rutas y modelos
    with app.app_context():
        from app import routes, models
        from init_db import seed_services
        db.create_all()
        seed_services()
    return app
