from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Optional, Length


class PatientForm(FlaskForm):
    nom            = StringField('Nom', validators=[DataRequired(), Length(max=64)])
    prenom         = StringField('Prénom', validators=[DataRequired(), Length(max=64)])
    date_naissance = DateField('Date de naissance', validators=[DataRequired()])
    sexe           = SelectField('Sexe', choices=[('M', 'Masculin'), ('F', 'Féminin')],
                                 validators=[DataRequired()])
    telephone      = StringField('Téléphone', validators=[Optional(), Length(max=20)])
    adresse        = StringField('Adresse', validators=[Optional(), Length(max=200)])
    submit         = SubmitField('Enregistrer')
