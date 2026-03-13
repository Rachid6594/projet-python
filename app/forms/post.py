from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title   = StringField('Titre', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Contenu', validators=[DataRequired()])
    submit  = SubmitField('Publier')
