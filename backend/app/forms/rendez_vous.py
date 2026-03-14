from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.fields import DateField, TimeField
from wtforms.validators import DataRequired, Optional, Length


class RendezVousForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    medecin_id = SelectField('Médecin', coerce=int, validators=[DataRequired()])
    date       = DateField('Date', validators=[DataRequired()])
    heure      = TimeField('Heure', validators=[DataRequired()])
    motif      = StringField('Motif', validators=[Optional(), Length(max=200)])
    statut     = SelectField('Statut', choices=[
                    ('programme', 'Programmé'),
                    ('effectue', 'Effectué'),
                    ('annule', 'Annulé')
                 ], default='programme')
    submit     = SubmitField('Enregistrer')
