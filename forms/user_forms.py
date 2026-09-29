from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message="El usuario es obligatorio."), Length(min=3, max=50)])
    email = StringField('Correo Electrónico', validators=[DataRequired(message="El correo es obligatorio."), Email(message="Correo inválido.")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="La contraseña es obligatoria."), Length(min=6, message="Mínimo 6 caracteres.")])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas no coinciden.')])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class EditUserForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Guardar Cambios')