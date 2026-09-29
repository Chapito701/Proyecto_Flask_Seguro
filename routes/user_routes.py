from flask import Blueprint, render_template, redirect, url_for, flash, session
from models.user import db, User
from forms.user_forms import RegisterForm, LoginForm, EditUserForm
from functools import wraps

user_bp = Blueprint('user', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para realizar esta acción.', 'warning')
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/')
def index():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()
        if existing_user:
            flash('El correo o usuario ya está registrado.', 'danger')
            return render_template('register.html', form=form)
        
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'¡Bienvenido de nuevo, {user.username}!', 'success')
            return redirect(url_for('user.index'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

@user_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('user.index'))

@user_bp.route('/profile/<int:id>')
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)

@user_bp.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    if session.get('user_id') != user.id:
        flash('No tienes permiso para editar este perfil.', 'danger')
        return redirect(url_for('user.index'))
        
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        session['username'] = user.username
        flash('¡Perfil actualizado con éxito!', 'success')
        return redirect(url_for('user.profile', id=user.id))
    return render_template('edit_profile.html', form=form, user=user)

@user_bp.route('/profile/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if session.get('user_id') != user.id:
        flash('No tienes permiso para eliminar esta cuenta.', 'danger')
        return redirect(url_for('user.index'))
        
    db.session.delete(user)
    db.session.commit()
    session.clear()
    flash('Usuario eliminado correctamente.', 'info')
    return redirect(url_for('user.index'))