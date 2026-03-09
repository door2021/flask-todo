from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from app.utils.email import send_password_reset_email

auth = Blueprint('auth', __name__)

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Signed in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/sign_in_page.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please sign in.', 'danger')
            return redirect(url_for('auth.sign_up'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return redirect(url_for('auth.sign_up'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please sign in.', 'success')
        return redirect(url_for('auth.sign_in'))
    
    return render_template('auth/sign_up_page.html')

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            send_password_reset_email(user)
            flash('If that email exists, a password reset link has been sent.', 'success')
            return redirect(url_for('auth.sign_in'))
        else:
            flash('If that email exists, a password reset link has been sent.', 'info')
            return redirect(url_for('auth.sign_in'))
    
    return render_template('auth/forget_password_page.html')

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))
    
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.is_reset_token_valid():
        flash('Invalid or expired reset link. Please request a new one.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.reset_password', token=token))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return redirect(url_for('auth.reset_password', token=token))
        
        user.set_password(password)
        user.clear_reset_token()
        db.session.commit()
        
        flash('Password reset successfully! Please sign in.', 'success')
        return redirect(url_for('auth.sign_in'))
    
    return render_template('auth/reset_password.html', token=token)

@auth.route('/sign-out')
@login_required
def sign_out():
    logout_user()
    flash('You have been signed out', 'info')
    return redirect(url_for('auth.sign_in'))