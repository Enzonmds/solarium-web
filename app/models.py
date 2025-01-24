from app import db
from datetime import datetime

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Service {self.name}>"
    
    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    service = db.relationship('Service', backref=db.backref('reservations', lazy=True))

    def __repr__(self):
        return f"<Reservation {self.client_name} - {self.date}>"
    




def seed_services():
    services_data = [
        {"name": "Corte de cabello", "description": "Corte clásico y moderno", "price": 1500},
        {"name": "Tratamiento facial", "description": "Limpieza profunda para rejuvenecer la piel", "price": 2000},
        {"name": "Solarium", "description": "Bronceado uniforme y seguro", "price": 2500}
    ]

    for service_data in services_data:
        # Verificar si el servicio ya existe
        if not Service.query.filter_by(name=service_data['name']).first():
            new_service = Service(**service_data)
            db.session.add(new_service)

    db.session.commit()
