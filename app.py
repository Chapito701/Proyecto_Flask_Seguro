from flask import Flask
from models.user import db
from routes.user_routes import user_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_proyecto_u1'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola123@localhost/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)