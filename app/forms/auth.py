from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User


class RegisterForm(FlaskForm):
    username         = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=3, max=64)])
    email            = StringField('Email', validators=[DataRequired(), Email()])
    password         = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmer', validators=[DataRequired(), EqualTo('password')])
    submit           = SubmitField('S\'inscrire')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Cet email est déjà utilisé.')


class LoginForm(FlaskForm):
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit   = SubmitField('Se connecter')
