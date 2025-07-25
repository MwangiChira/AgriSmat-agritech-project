# app/ml/predict.py

import torch
from torchvision import transforms
from PIL import Image

# (In a real app, load trained PyTorch models. Here we illustrate stubs.)
try:
    # Example: load a pretrained crop recommendation model (if exists)
    crop_model = torch.load('app/models/crop_predictor.pt')
    crop_model.eval()
except Exception:
    crop_model = None

try:
    disease_model = torch.load('app/models/disease_detector.pt')
    disease_model.eval()
except Exception:
    disease_model = None

def predict_crop(soil_data):
    """
    Predicts an optimal crop type given soil properties.
    For MVP, this returns a dummy value or uses a simple rule.
    """
    # TODO: replace with real model prediction
    ph = soil_data.get('ph', 7)
    if ph < 6.0:
        return "Maize"
    else:
        return "Wheat"

def detect_disease(image_path):
    """
    Detects crop disease from an image using a CNN.
    """
    if disease_model is None:
        return "No model available (demo mode)"
    # Example of real preprocessing if model exists:
    image = Image.open(image_path).convert('RGB')
    preprocess = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
    ])
    img_t = preprocess(image).unsqueeze(0)  # create batch dimension
    with torch.no_grad():
        outputs = disease_model(img_t)
        _, predicted = outputs.max(1)
    # Map 'predicted' index to disease name (need a label map)
    label = "DiseaseID_" + str(predicted.item())
    return label

def get_weather(location):
    """
    Fetches weather forecast for the given location.
    """
    # For MVP, return dummy forecast.
    # In production, call OpenWeatherMap API here.
    return {
        '7_day_forecast': [
            {'day': 'Monday', 'rain': '10%', 'temp': '25°C'},
            {'day': 'Tuesday', 'rain': '0%', 'temp': '27°C'},
            # ... etc ...
        ]
    }
