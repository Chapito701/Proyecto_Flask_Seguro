from flask import Blueprint, render_template, redirect, url_for, flash
from models.user import db, User
from forms.user_forms import RegisterForm, LoginForm, EditUserForm
from flask_login import login_user, logout_user, login_required, current_user

user_bp = Blueprint('user', __name__)

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
            # 3.4 Iniciar sesión con login_user
            login_user(user)
            flash(f'¡Bienvenido de nuevo, {user.username}!', 'success')
            return redirect(url_for('user.index'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

@user_bp.route('/logout')
@login_required
def logout():
    # 3.4 Cerrar sesión con logout_user
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('user.index'))

@user_bp.route('/profile/<int:id>')
@login_required # 4. Protección de rutas
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)

@user_bp.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    # Verificación usando current_user
    if current_user.id != user.id:
        flash('No tienes permiso para editar este perfil.', 'danger')
        return redirect(url_for('user.index'))
        
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('¡Perfil actualizado con éxito!', 'success')
        return redirect(url_for('user.profile', id=user.id))
    return render_template('edit_profile.html', form=form, user=user)

@user_bp.route('/profile/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if current_user.id != user.id:
        flash('No tienes permiso para eliminar esta cuenta.', 'danger')
        return redirect(url_for('user.index'))
        
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash('Usuario eliminado correctamente.', 'info')
    return redirect(url_for('user.index'))