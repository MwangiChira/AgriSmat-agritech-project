# app/ml/predict.py

import os
import requests
from PIL import Image
import random

def predict_crop(soil_data):
    """
    Predicts an optimal crop type given soil properties.
    This is a simplified rule-based system for demonstration.
    In production, this would use a trained ML model.
    """
    ph = soil_data.get('ph', 7.0)
    nitrogen = soil_data.get('nitrogen', 50)
    phosphorus = soil_data.get('phosphorus', 30)
    potassium = soil_data.get('potassium', 40)
    soil_type = soil_data.get('soil_type', 'loamy')
    
    # Simple rule-based crop recommendation
    if soil_type == 'clay':
        if ph >= 6.0 and ph <= 7.5:
            if nitrogen >= 40:
                return "Rice"
            else:
                return "Wheat"
        else:
            return "Barley"
    
    elif soil_type == 'sandy':
        if ph >= 6.0 and ph <= 8.0:
            if potassium >= 35:
                return "Millet"
            else:
                return "Groundnut"
        else:
            return "Sweet Potato"
    
    else:  # loamy soil
        if ph >= 6.0 and ph <= 7.0:
            if nitrogen >= 50 and phosphorus >= 25:
                return "Maize"
            elif potassium >= 40:
                return "Tomato"
            else:
                return "Bean"
        elif ph > 7.0:
            return "Sunflower"
        else:
            return "Potato"

def detect_disease(image_path):
    """
    Detects crop disease from an image.
    This is a placeholder implementation.
    In production, this would use a trained CNN model.
    """
    try:
        # Verify image exists and can be opened
        if not os.path.exists(image_path):
            return "Error: Image file not found"
        
        # Try to open and verify it's a valid image
        with Image.open(image_path) as img:
            # Get image dimensions for basic validation
            width, height = img.size
            
            # Simple mock disease detection based on image properties
            # In reality, this would be a trained deep learning model
            diseases = [
                "Healthy - No disease detected",
                "Early Blight - Apply copper-based fungicide",
                "Late Blight - Improve drainage and air circulation", 
                "Leaf Spot - Remove affected leaves and apply fungicide",
                "Powdery Mildew - Reduce humidity and apply sulfur spray",
                "Rust - Apply appropriate fungicide treatment"
            ]
            
            # Mock prediction based on image size (just for demo)
            prediction_index = (width + height) % len(diseases)
            return diseases[prediction_index]
            
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def get_weather(location):
    """
    Fetches weather forecast for the given location.
    This is a mock implementation. In production, integrate with
    a weather API like OpenWeatherMap.
    """
    try:
        # Mock weather data - in production, call actual weather API
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        forecast = []
        for i, day in enumerate(days):
            # Generate mock weather data
            temp_base = 25 + random.randint(-5, 10)
            rain_chance = random.choice(['0%', '10%', '20%', '30%', '60%', '80%'])
            
            forecast.append({
                'day': day,
                'temp': f'{temp_base}°C',
                'rain': rain_chance
            })
        
        return {
            '7_day_forecast': forecast,
            'location': location
        }
        
    except Exception as e:
        # Fallback weather data
        return {
            '7_day_forecast': [
                {'day': 'Monday', 'rain': '10%', 'temp': '25°C'},
                {'day': 'Tuesday', 'rain': '0%', 'temp': '27°C'},
                {'day': 'Wednesday', 'rain': '20%', 'temp': '24°C'},
                {'day': 'Thursday', 'rain': '5%', 'temp': '26°C'},
                {'day': 'Friday', 'rain': '30%', 'temp': '23°C'},
                {'day': 'Saturday', 'rain': '60%', 'temp': '22°C'},
                {'day': 'Sunday', 'rain': '40%', 'temp': '24°C'},
            ],
            'location': location
        }

def get_farming_tips(crop, soil_data, weather_data):
    """
    Provides farming tips based on recommended crop, soil conditions, and weather.
    """
    tips = []
    
    # Crop-specific tips
    crop_tips = {
        'Maize': [
            'Plant during the rainy season for optimal growth',
            'Ensure proper spacing of 75cm between rows',
            'Apply nitrogen fertilizer at planting and during growth'
        ],
        'Rice': [
            'Maintain water level of 2-5cm in paddy fields',
            'Transplant seedlings after 20-25 days',
            'Apply phosphorus fertilizer before planting'
        ],
        'Wheat': [
            'Plant in well-drained soil with good organic matter',
            'Optimal planting time is October-December',
            'Apply balanced NPK fertilizer'
        ]
    }
    
    if crop in crop_tips:
        tips.extend(crop_tips[crop])
    
    # Soil-based tips
    ph = soil_data.get('ph', 7.0)
    if ph < 6.0:
        tips.append('Consider adding lime to increase soil pH')
    elif ph > 8.0:
        tips.append('Consider adding organic matter to lower soil pH')
    
    # Weather-based tips
    if weather_data and '7_day_forecast' in weather_data:
        high_rain_days = sum(1 for day in weather_data['7_day_forecast'] 
                           if int(day['rain'].replace('%', '')) > 50)
        if high_rain_days >= 3:
            tips.append('High rainfall expected - ensure proper drainage')
            tips.append('Consider fungicide application to prevent diseases')
    
    return tips