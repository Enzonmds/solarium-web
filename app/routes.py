from flask import render_template, request, redirect, url_for, flash
from app import db  
from app.forms import ReservationForm
from app.models import Reservation, Service
from flask import jsonify
from datetime import datetime, timedelta
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


@app.route('/api/availability', methods=['GET'])
def check_availability():
    # Obtener los parámetros de fecha y servicio
    service_id = request.args.get('service_id', type=int)
    date_str = request.args.get('date', type=str)

    # Convertir la fecha a un objeto datetime
    date = datetime.strptime(date_str, '%Y-%m-%d')
    start_time = datetime(date.year, date.month, date.day, 11, 0)
    end_time = datetime(date.year, date.month, date.day, 19, 30)
    delta = timedelta(minutes=20)

    # Calcular todos los horarios posibles
    available_slots = []
    current_time = start_time
    while current_time <= end_time:
        available_slots.append(current_time)
        current_time += delta

    # Obtener reservas del día
    reservations = Reservation.query.filter(
        db.func.date(Reservation.date) == date.date(),
        Reservation.service_id == service_id
    ).all()
    
    reserved_times = [res.date for res in reservations]

    # Filtrar horarios ocupados
    free_slots = [slot for slot in available_slots if slot not in reserved_times]

    return jsonify({
        'available_slots': [slot.isoformat() for slot in free_slots]
    })


@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    reservations = Reservation.query.all()
    events = []
    for reservation in reservations:
        events.append({
            'title': f'{reservation.client_name} - {reservation.service.name}',
            'start': reservation.date.isoformat()  # Convertimos la fecha a formato ISO
        })
    return jsonify(events)

@app.route('/calendar', methods=['GET'])
def calendar():
    return render_template('calendar.html')


@app.route('/appointments')
def appointments():

    return render_template('appointments.html')

@app.route('/blog')
def blog():
    
    return render_template('blog.html')
