from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional


class ConsultationForm(FlaskForm):
    symptomes    = TextAreaField('Symptômes', validators=[Optional()])
    diagnostic   = TextAreaField('Diagnostic', validators=[DataRequired()])
    traitement   = TextAreaField('Traitement prescrit', validators=[Optional()])
    observations = TextAreaField('Observations', validators=[Optional()])
    submit       = SubmitField('Enregistrer la consultation')
