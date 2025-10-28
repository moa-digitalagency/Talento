from flask_mail import Message
from flask import render_template
from app import mail
import secrets
import string

def generate_random_password(unique_code=None, length=12):
    """
    Generate a password - uses unique_code if provided, otherwise generates random
    
    Args:
        unique_code: If provided, will be used as the password
        length: Length of random password if unique_code not provided
    
    Returns:
        Password string
    """
    if unique_code:
        return unique_code
    
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def send_confirmation_email(user, password):
    """Send confirmation email with login credentials"""
    msg = Message(
        'Bienvenue sur TalentsMaroc.com - Votre profil a été créé',
        recipients=[user.email]
    )
    
    msg.html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
                <h2 style="color: #3B82F6;">Bienvenue sur TalentsMaroc.com !</h2>
                <p>Bonjour {user.full_name},</p>
                <p>Votre profil de talent a été créé avec succès. Voici vos informations de connexion :</p>
                
                <div style="background-color: white; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Identifiant unique :</strong> {user.formatted_code}</p>
                    <p><strong>Email :</strong> {user.email}</p>
                    <p><strong>Mot de passe temporaire :</strong> {password}</p>
                </div>
                
                <p>Pour des raisons de sécurité, nous vous recommandons de changer votre mot de passe lors de votre première connexion.</p>
                
                <p>Vous pouvez accéder à votre espace personnel en cliquant sur le lien ci-dessous :</p>
                <p style="text-align: center; margin: 30px 0;">
                    <a href="#" style="background-color: #3B82F6; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Accéder à mon profil</a>
                </p>
                
                <p>Merci de votre confiance !</p>
                <p>L'équipe TalentsMaroc.com</p>
            </div>
        </body>
    </html>
    """
    
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
