from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeLocalField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email
from app.models import Service, Reservation
from datetime import datetime


class ReservationForm(FlaskForm):
    client_name = StringField('Nombre del Cliente', validators=[DataRequired()])
    client_email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    service_id = SelectField('Servicio', coerce=int, validators=[DataRequired()])
    date = DateTimeLocalField('Fecha y Hora', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Reservar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar servicios en el campo de selección
        self.service_id.choices = [(service.id, service.name) for service in Service.query.all()]

    def validate_date(self, field):

        if field.data <= datetime.now():
            raise ValidationError("La fecha y hora deben ser futuras.")
        
        # Verificar que no exista una reserva para el mismo servicio, cliente y fecha
        existing_reservation = Reservation.query.filter_by(
            service_id=self.service_id.data,
            date=field.data
        ).first()
        if existing_reservation:
            raise ValidationError("Ya existe una reserva para este servicio en la fecha y hora seleccionadas.")
        

