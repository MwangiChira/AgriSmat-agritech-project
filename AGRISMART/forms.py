# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class FarmForm(FlaskForm):
    """WTForms form for farm input: soil data, location, image."""
    soil_type = SelectField('Soil Type', choices=[
        ('loamy', 'Loamy'), ('sandy', 'Sandy'), ('clay', 'Clay')], 
        validators=[DataRequired()])
    ph = FloatField('Soil pH', validators=[DataRequired()])
    nitrogen = FloatField('Nitrogen (ppm)', validators=[DataRequired()])
    phosphorus = FloatField('Phosphorus (ppm)', validators=[DataRequired()])
    potassium = FloatField('Potassium (ppm)', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    image = FileField('Upload Crop Image', validators=[FileAllowed(['jpeg','png,'jpg'], 'Images only!')])
    submit = SubmitField('Get Insights')
