from flask import Flask, render_template
from models.user import db, User
from routes.user_routes import user_bp
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_proyecto_u1'

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola123@localhost/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 5. Gestión de sesiones seguras (Configuración de Cookies)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

db.init_app(app)

# 3.3 Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(user_bp)

# 7. Manejadores de error 401 y 403
@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('401.html'), 401

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)