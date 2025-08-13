# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileAllowed

class FarmForm(FlaskForm):
    """WTForms form for farm input: soil data, location, image."""
    soil_type = SelectField('Soil Type', choices=[
        ('loamy', 'Loamy'), 
        ('sandy', 'Sandy'), 
        ('clay', 'Clay')
    ], validators=[DataRequired()])
    
    ph = FloatField('Soil pH', validators=[
        DataRequired(), 
        NumberRange(min=0, max=14, message="pH must be between 0 and 14")
    ])
    
    nitrogen = FloatField('Nitrogen (ppm)', validators=[
        DataRequired(),
        NumberRange(min=0, message="Nitrogen must be positive")
    ])
    
    phosphorus = FloatField('Phosphorus (ppm)', validators=[
        DataRequired(),
        NumberRange(min=0, message="Phosphorus must be positive")
    ])
    
    potassium = FloatField('Potassium (ppm)', validators=[
        DataRequired(),
        NumberRange(min=0, message="Potassium must be positive")
    ])
    
    location = StringField('Location', validators=[DataRequired()])
    
    image = FileField('Upload Crop Image', validators=[
        FileAllowed(['jpeg', 'jpg', 'png'], 'Images only!')
    ])
    
    submit = SubmitField('Get Insights')