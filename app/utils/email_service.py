from flask_mail import Message
from flask import render_template
from app import mail
import secrets
import string

def generate_random_password(simple_format=True):
    """
    Generate a password
    
    Args:
        simple_format: If True, generates "Talent" + 6 random digits (e.g., Talent123456)
                      If False, generates a complex random password
    
    Returns:
        Password string
    """
    if simple_format:
        # Format simple mais sécurisé: Talent + 6 chiffres aléatoires
        # Donne 1,000,000 de combinaisons possibles
        random_digits = ''.join(secrets.choice(string.digits) for _ in range(6))
        return f"Talent{random_digits}"
    
    # Format complexe (pour usage futur si nécessaire)
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(12))
    return password

def send_confirmation_email(user, password):
    """Send confirmation email with login credentials"""
    msg = Message(
        'Bienvenue sur taalentio.com - Votre profil a été créé',
        recipients=[user.email]
    )
    
    msg.html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
                <h2 style="color: #3B82F6;">Bienvenue sur taalentio.com !</h2>
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
                <p>L'équipe taalentio.com</p>
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
