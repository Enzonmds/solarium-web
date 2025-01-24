from flask import render_template, request, redirect, url_for, flash
from app import db  
from app.forms import ReservationForm
from app.models import Reservation, Service
from flask import current_app as app


# Rutas básicas
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    
    services = Service.query.all()
    return render_template('services.html', services=services)


@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    form = ReservationForm()
    if form.validate_on_submit():
        # Crear nueva reserva
        reservation = Reservation(
            client_name=form.client_name.data,
            client_email=form.client_email.data,
            service_id=form.service_id.data,
            date=form.date.data
        )
        db.session.add(reservation)
        db.session.commit()
        flash('Reserva realizada con éxito', 'success')
        return redirect(url_for('reservations'))
    
    # Recuperar todas las reservas existentes
    reservations = Reservation.query.order_by(Reservation.date).all()
    return render_template('reservations.html', form=form, reservations=reservations)