from app import create_app, db
from app.models import seed_services

app = create_app()

with app.app_context():
    print("Inicializando la base de datos...")
    db.create_all()  # Crear las tablas
    seed_services()  # Poblar la base de datos con servicios iniciales
    print("Base de datos inicializada con éxito.")
