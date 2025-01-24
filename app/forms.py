from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Email
from app.models import Service

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
