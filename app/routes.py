from flask import render_template, request, redirect, url_for
from app import db  
from app.models import Service
from flask import current_app as app  

# Rutas básicas
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    
    services = Service.query.all()
    return render_template('services.html', services=services)
