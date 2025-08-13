# app/routes.py

import os
from flask import Blueprint, render_template, request, current_app, flash
from werkzeug.utils import secure_filename
from .forms import FarmForm
from .ml.predict import predict_crop, detect_disease, get_weather

# Define a Flask Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def home():
    """
    Home page: displays form and handles form submission.
    Farmers enter soil data, location, and optionally an image.
    On POST, we compute predictions and show results.
    """
    form = FarmForm()
    
    if form.validate_on_submit():
        # Gather form data
        soil_data = {
            'nitrogen': form.nitrogen.data,
            'phosphorus': form.phosphorus.data,
            'potassium': form.potassium.data,
            'ph': form.ph.data,
            'location': form.location.data.strip(),
            'soil_type': form.soil_type.data
        }
        
        # Perform crop prediction
        crop_rec = predict_crop(soil_data)
        
        # Handle uploaded image for disease detection
        disease_result = None
        image_filename = None
        
        if form.image.data:
            file = form.image.data
            if file.filename != '':
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                image_path = os.path.join(upload_path, filename)
                file.save(image_path)
                image_filename = filename
                disease_result = detect_disease(image_path)
        
        # Get weather forecast
        forecast = get_weather(soil_data['location'])
        
        # Render results page
        return render_template('results.html', 
                               crop=crop_rec,
                               disease=disease_result,
                               weather=forecast,
                               soil_data=soil_data,
                               image_filename=image_filename)
    
    # On GET or validation failure, show the input form
    return render_template('home.html', form=form)