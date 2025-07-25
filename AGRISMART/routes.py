# app/routes.py

from flask import Blueprint, render_template, request
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
            'location': form.location.data.strip().lower(),
            'soil_type': form.soil_type.data
        }
        # Perform predictions (stub or call ML functions)
        crop_rec = predict_crop(soil_data)  # e.g., returns "Maize"
        
        # Handle uploaded image for disease detection
        disease_result = None
        if form.image.data:
            file = form.image.data
            filename = file.filename
            image_path = 'static/uploads/' + filename
            file.save(image_path)  # Save to static folder
            disease_result = detect_disease(image_path)
        
        # Get weather forecast
        forecast = get_weather(soil_data['location'])
        
        # Render results page
        return render_template('results.html', 
                               crop=crop_rec,
                               disease=disease_result,
                               weather=forecast)
    # On GET or validation failure, just show the input form
    return render_template('home.html', form=form)
