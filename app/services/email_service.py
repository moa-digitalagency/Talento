"""
Service d'envoi d'emails avec SendGrid
"""
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
from flask import current_app, render_template

def get_application_domain():
    """
    Détecte le domaine de l'application selon l'environnement (Replit, VPS, ou autre)
    
    Returns:
        str: Le domaine de l'application (ex: 'talentsmaroc.com' ou 'app-name.replit.app')
    """
    # 1. Essayer d'abord la variable d'environnement personnalisée (pour VPS)
    domain = os.environ.get('APP_DOMAIN')
    if domain:
        return domain
    
    # 2. Essayer le domaine Replit (pour déploiements Replit)
    domain = os.environ.get('REPLIT_DEV_DOMAIN')
    if domain:
        return domain
    
    # 3. Essayer REPLIT_DOMAINS (format: domain1.repl.co,domain2.repl.co)
    domains = os.environ.get('REPLIT_DOMAINS')
    if domains:
        return domains.split(',')[0].strip()
    
    # 4. Fallback: localhost avec port
    return 'localhost:5000'

class EmailService:
    """Service pour l'envoi d'emails via SendGrid"""
    
    def __init__(self, api_key=None, from_email=None):
        # Essayer d'abord AppSettings, puis les variables d'environnement
        try:
            from app.models.settings import AppSettings
            self.api_key = api_key or AppSettings.get('sendgrid_api_key') or os.environ.get('SENDGRID_API_KEY')
            self.from_email = from_email or AppSettings.get('sender_email') or os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@myoneart.com')
        except:
            self.api_key = api_key or os.environ.get('SENDGRID_API_KEY')
            self.from_email = from_email or os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@myoneart.com')
    
    def _get_logo_base64(self):
        """
        Encode le logo en base64 pour l'inclure dans les emails
        
        Returns:
            str: Logo encodé en base64, ou None si le logo n'existe pas
        """
        logo_paths = [
            'app/static/img/logo-full.png',
            'static/img/logo-full.png'
        ]
        
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                try:
                    with open(logo_path, 'rb') as f:
                        logo_data = base64.b64encode(f.read()).decode()
                        return logo_data
                except Exception as e:
                    current_app.logger.warning(f"Erreur lecture logo {logo_path}: {str(e)}")
                    continue
        
        return None
        
    def send_email(self, to_email, subject, html_content, attachments=None):
        """
        Envoie un email via SendGrid
        
        Args:
            to_email: Email du destinataire
            subject: Sujet de l'email
            html_content: Contenu HTML de l'email
            attachments: Liste de dictionnaires avec 'content', 'filename', 'type'
        
        Returns:
            True si envoyé avec succès, False sinon
        """
        # Récupérer la clé API à chaque envoi pour supporter la mise à jour à chaud
        api_key = self.api_key
        from_email = self.from_email
        
        try:
            from app.models.settings import AppSettings
            api_key = AppSettings.get('sendgrid_api_key') or api_key
            from_email = AppSettings.get('sender_email') or from_email
        except:
            pass
        
        if not api_key:
            error_msg = "❌ SendGrid API key manquante. Configurez SENDGRID_API_KEY dans les variables d'environnement ou dans /admin/settings/api-keys"
            current_app.logger.error(error_msg)
            print(f"🔴 {error_msg}")
            return False
        
        if not from_email:
            error_msg = "❌ Email expéditeur manquant. Configurez SENDGRID_FROM_EMAIL"
            current_app.logger.error(error_msg)
            print(f"🔴 {error_msg}")
            return False
        
        print(f"📧 Tentative d'envoi email à: {to_email}")
        print(f"📤 Expéditeur: {from_email}")
        print(f"📝 Sujet: {subject}")
        print(f"🔑 API Key (premiers 8 chars): {api_key[:8] if api_key else 'None'}...")
            
        try:
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )
            
            if attachments:
                for att in attachments:
                    attachment = Attachment(
                        FileContent(att['content']),
                        FileName(att['filename']),
                        FileType(att['type']),
                        Disposition('attachment')
                    )
                    message.add_attachment(attachment)
            
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                success_msg = f"✅ Email envoyé avec succès à {to_email}"
                current_app.logger.info(success_msg)
                print(success_msg)
                return True
            else:
                error_msg = f"❌ Erreur SendGrid - Code: {response.status_code}, Body: {response.body}"
                current_app.logger.error(error_msg)
                print(f"🔴 {error_msg}")
                return False
                
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            error_msg = f"❌ Erreur SendGrid: {str(e)}"
            current_app.logger.error(f"{error_msg}\n{error_details}")
            print(f"🔴 ERREUR SENDGRID DÉTAILLÉE:")
            print(f"   Message: {str(e)}")
            print(f"   Type: {type(e).__name__}")
            print(f"   API Key présente: {bool(self.api_key)}")
            print(f"   From Email: {self.from_email}")
            print(f"   Traceback:\n{error_details}")
            return False
    
    def send_application_confirmation(self, user, profile_pdf_path=None):
        """
        Envoie l'email de confirmation de candidature avec le PDF du profil
        
        Args:
            user: Objet User
            profile_pdf_path: Chemin vers le PDF du profil (optionnel)
        
        Returns:
            True si envoyé, False sinon
        """
        try:
            domain = get_application_domain()
            profile_url = f"https://{domain}/profile/view/{user.unique_code}"
            
            # Encoder le logo en base64 pour l'email
            logo_base64 = self._get_logo_base64()
            logo_img = f'<img src="data:image/png;base64,{logo_base64}" alt="taalentio.com" style="max-width: 250px; height: auto; margin-bottom: 15px;">' if logo_base64 else ''
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .button {{ display: inline-block; background: #667eea; color: white; 
                              padding: 12px 30px; text-decoration: none; border-radius: 5px; 
                              margin: 20px 0; }}
                    .code {{ background: #fff; border: 2px dashed #667eea; padding: 15px; 
                            font-size: 24px; font-weight: bold; text-align: center; 
                            color: #667eea; margin: 20px 0; border-radius: 5px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>⭐ Bienvenue sur taalentio.com !</h1>
                    </div>
                    <div class="content">
                        <h2>Bonjour {user.full_name},</h2>
                        <p>Nous avons bien reçu votre candidature sur la plateforme taalentio.com !</p>
                        
                        <p>Votre profil de talent a été créé avec succès. Voici votre code unique :</p>
                        <div class="code">{user.unique_code}</div>
                        
                        <p>Vous pouvez consulter votre profil public à tout moment via ce lien :</p>
                        <div style="text-align: center;">
                            <a href="{profile_url}" class="button">Voir mon profil</a>
                        </div>
                        
                        <p>Vous recevrez sous peu vos identifiants de connexion pour accéder à votre 
                           espace personnel et modifier votre profil.</p>
                        
                        <p style="margin-top: 30px;">Cordialement,<br>
                        <strong>L'équipe taalentio.com</strong></p>
                    </div>
                    <div class="footer">
                        <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            attachments = []
            if profile_pdf_path and os.path.exists(profile_pdf_path):
                with open(profile_pdf_path, 'rb') as f:
                    pdf_content = base64.b64encode(f.read()).decode()
                    attachments.append({
                        'content': pdf_content,
                        'filename': f'profil_{user.unique_code}.pdf',
                        'type': 'application/pdf'
                    })
            
            return self.send_email(
                to_email=user.email,
                subject=f"✅ Candidature reçue - Votre code taalentio.com : {user.unique_code}",
                html_content=html_content,
                attachments=attachments if attachments else None
            )
            
        except Exception as e:
            current_app.logger.error(f"Erreur envoi confirmation: {str(e)}")
            return False
    
    def send_login_credentials(self, user, password):
        """
        Envoie les identifiants de connexion (code unique + mot de passe)
        
        Args:
            user: Objet User
            password: Mot de passe en clair (généré)
        
        Returns:
            True si envoyé, False sinon
        """
        try:
            domain = get_application_domain()
            login_url = f"https://{domain}/login"
            
            # Encoder le logo en base64 pour l'email
            logo_base64 = self._get_logo_base64()
            logo_img = f'<img src="data:image/png;base64,{logo_base64}" alt="taalentio.com" style="max-width: 250px; height: auto; margin-bottom: 15px;">' if logo_base64 else ''
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .button {{ display: inline-block; background: #667eea; color: white; 
                              padding: 12px 30px; text-decoration: none; border-radius: 5px; 
                              margin: 20px 0; }}
                    .credentials {{ background: #fff; border: 2px solid #667eea; padding: 20px; 
                                   border-radius: 5px; margin: 20px 0; }}
                    .credential-item {{ margin: 15px 0; }}
                    .credential-label {{ color: #666; font-size: 14px; }}
                    .credential-value {{ background: #f0f0f0; padding: 10px; border-radius: 3px; 
                                        font-family: monospace; font-size: 16px; margin-top: 5px; }}
                    .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; 
                               padding: 15px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>🔐 Vos identifiants taalentio.com</h1>
                    </div>
                    <div class="content">
                        <h2>Bonjour {user.full_name},</h2>
                        <p>Voici vos identifiants de connexion pour accéder à votre espace personnel sur taalentio.com :</p>
                        
                        <div class="credentials">
                            <div class="credential-item">
                                <div class="credential-label">Identifiant (Code unique)</div>
                                <div class="credential-value">{user.unique_code}</div>
                            </div>
                            <div class="credential-item">
                                <div class="credential-label">Mot de passe</div>
                                <div class="credential-value">{password}</div>
                            </div>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Important :</strong> Ce mot de passe est temporaire. 
                            <strong>Nous vous recommandons vivement de le changer dès votre première connexion</strong> 
                            depuis votre profil pour sécuriser votre compte.
                        </div>
                        
                        <div style="text-align: center;">
                            <a href="{login_url}" class="button">Se connecter</a>
                        </div>
                        
                        <p style="margin-top: 30px;"><strong>Que pouvez-vous faire dans votre espace ?</strong></p>
                        <ul>
                            <li>Consulter votre profil public</li>
                            <li>Modifier vos informations personnelles</li>
                            <li>Mettre à jour vos compétences et talents</li>
                            <li>Télécharger votre QR code</li>
                        </ul>
                        
                        <p style="margin-top: 30px;">Cordialement,<br>
                        <strong>L'équipe taalentio.com</strong></p>
                    </div>
                    <div class="footer">
                        <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return self.send_email(
                to_email=user.email,
                subject="🔐 Vos identifiants de connexion taalentio.com",
                html_content=html_content
            )
            
        except Exception as e:
            current_app.logger.error(f"Erreur envoi identifiants: {str(e)}")
            return False
    
    def send_test_email(self, to_email):
        """
        Envoie un email de test pour vérifier la configuration SendGrid
        
        Args:
            to_email: Email du destinataire
        
        Returns:
            True si envoyé, False sinon
        """
        try:
            # Encoder le logo en base64 pour l'email
            logo_base64 = self._get_logo_base64()
            logo_img = f'<img src="data:image/png;base64,{logo_base64}" alt="taalentio.com" style="max-width: 250px; height: auto; margin-bottom: 15px;">' if logo_base64 else ''
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                              color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .success {{ background: #d1fae5; border-left: 4px solid #10b981; 
                               padding: 15px; margin: 20px 0; border-radius: 5px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>✅ Email de Test taalentio.com</h1>
                    </div>
                    <div class="content">
                        <div class="success">
                            <strong>✨ Félicitations !</strong> La configuration SendGrid fonctionne correctement.
                        </div>
                        
                        <p>Cet email de test confirme que :</p>
                        <ul>
                            <li>✅ La clé API SendGrid est valide</li>
                            <li>✅ L'email expéditeur est correctement configuré</li>
                            <li>✅ Les emails peuvent être envoyés depuis taalentio.com</li>
                        </ul>
                        
                        <p>Vous pouvez maintenant utiliser l'envoi automatique d'emails pour :</p>
                        <ul>
                            <li>Confirmer les nouvelles candidatures</li>
                            <li>Envoyer les identifiants de connexion</li>
                        </ul>
                        
                        <p style="margin-top: 30px;">Cordialement,<br>
                        <strong>L'équipe taalentio.com</strong></p>
                    </div>
                    <div class="footer">
                        <p>Cet email a été envoyé depuis la page de configuration de taalentio.com.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return self.send_email(
                to_email=to_email,
                subject="✅ Test de configuration SendGrid - taalentio.com",
                html_content=html_content
            )
            
        except Exception as e:
            current_app.logger.error(f"Erreur envoi test email: {str(e)}")
            return False

# Instance globale
email_service = EmailService()
