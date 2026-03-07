# app/utils/email.py
from flask import current_app
from flask_mail import Mail, Message
import threading

mail = Mail()

def send_async_email(app, msg):
    """Send email in background thread"""
    with app.app_context():
        mail.send(msg)

def send_password_reset_email(user):
    """Send password reset email to user"""
    token = user.generate_reset_token()
    
    # Build reset URL
    reset_url = f"{current_app.config.get('BASE_URL', 'http://localhost:5000')}/auth/reset-password/{token}"
    
    # Create email message
    msg = Message(
        subject='Reset Your Password - Todo App',
        sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
        recipients=[user.email]
    )
    
    # HTML body
    msg.html = f'''
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="color: white; margin: 0;">Todo App</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">Password Reset Request</p>
        </div>
        
        <div style="padding: 30px; background: #f8f9fa; border-radius: 0 0 10px 10px;">
            <h2 style="color: #333; margin-top: 0;">Hello {user.username}!</h2>
            
            <p style="color: #666; line-height: 1.6;">
                You requested to reset your password. Click the button below to set a new password:
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; 
                          padding: 12px 30px; 
                          text-decoration: none; 
                          border-radius: 5px; 
                          display: inline-block;
                          font-weight: bold;">
                    Reset Password
                </a>
            </div>
            
            <p style="color: #666; line-height: 1.6;">
                Or copy and paste this link into your browser:
                <br>
                <a href="{reset_url}" style="color: #667eea;">{reset_url}</a>
            </p>
            
            <p style="color: #999; font-size: 14px; margin-top: 30px;">
                ⚠️ This link will expire in 1 hour.
                <br>
                If you didn't request this, please ignore this email.
            </p>
        </div>
    </div>
    '''
    
    # Plain text fallback
    msg.body = f'''
    Hello {user.username},
    
    You requested to reset your password. Click the link below to set a new password:
    
    {reset_url}
    
    This link will expire in 1 hour.
    
    If you didn't request this, please ignore this email.
    
    - Todo App Team
    '''
    
    # Send in background thread
    thread = threading.Thread(target=send_async_email, args=(current_app._get_current_object(), msg))
    thread.start()
    
    return True