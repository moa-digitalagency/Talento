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
    
    def get_template_preview(self, template_type, data):
        """
        Génère un aperçu HTML d'un template email
        
        Args:
            template_type: Type de template à afficher
            data: Données d'exemple pour le template
            
        Returns:
            str: HTML du template ou None si template inconnu
        """
        logo_base64 = self._get_logo_base64()
        logo_img = f'<img src="data:image/png;base64,{logo_base64}" alt="taalentio.com" style="max-width: 250px; height: auto; margin-bottom: 15px;">' if logo_base64 else ''
        domain = get_application_domain()
        
        if template_type == 'talent_registration':
            profile_url = f"https://{domain}/profile/view/{data.get('unique_code', 'CODE123')}"
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #5b7ef5; border-radius: 10px; margin-top: 20px; }}
                    .button {{ display: inline-block; background: white; color: #5b7ef5; 
                              padding: 12px 30px; text-decoration: none; border: 2px solid #5b7ef5; 
                              border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .button:hover {{ background: #5b7ef5; color: white; }}
                    .code {{ background: #f5f5f5; border: 2px dashed #5b7ef5; padding: 15px; 
                            font-size: 24px; font-weight: bold; text-align: center; 
                            color: #5b7ef5; margin: 20px 0; border-radius: 5px; }}
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
                        <h2>Bonjour {data.get('full_name', 'Utilisateur')},</h2>
                        <p>Nous avons bien reçu votre candidature sur la plateforme taalentio.com !</p>
                        
                        <p>Voici votre <strong>code unique</strong> qui vous permettra d'accéder à votre profil :</p>
                        <div class="code">{data.get('unique_code', 'CODE123')}</div>
                        
                        <p>Vous pouvez consulter votre profil public à cette adresse :</p>
                        <div style="text-align: center;">
                            <a href="{profile_url}" class="button">🔍 Voir mon profil</a>
                        </div>
                        
                        <p><strong>Note importante :</strong> Conservez bien ce code, il vous sera demandé pour vous connecter à votre espace personnel.</p>
                        
                        <div class="footer">
                            <p>© 2024 taalentio.com - Plateforme de valorisation des talents</p>
                            <p>Ceci est un email automatique, merci de ne pas y répondre.</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
        
        elif template_type == 'cinema_talent_registration':
            profile_url = f"https://{domain}/cinema/profile/{data.get('unique_code', 'CODE123')}"
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #f5576c; border-radius: 10px; margin-top: 20px; }}
                    .button {{ display: inline-block; background: white; color: #f5576c; 
                              padding: 12px 30px; text-decoration: none; border: 2px solid #f5576c; 
                              border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .button:hover {{ background: #f5576c; color: white; }}
                    .code {{ background: #f5f5f5; border: 2px dashed #f5576c; padding: 15px; 
                            font-size: 24px; font-weight: bold; text-align: center; 
                            color: #f5576c; margin: 20px 0; border-radius: 5px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>🎬 Bienvenue au CINEMA de taalentio.com !</h1>
                    </div>
                    <div class="content">
                        <h2>Bonjour {data.get('full_name', 'Utilisateur')},</h2>
                        <p>Félicitations ! Votre inscription au module CINEMA a été validée avec succès.</p>
                        
                        <p>Votre <strong>code unique CINEMA</strong> :</p>
                        <div class="code">{data.get('unique_code', 'CODE123')}</div>
                        
                        <p>Consultez votre profil cinéma public :</p>
                        <div style="text-align: center;">
                            <a href="{profile_url}" class="button">🎭 Voir mon profil CINEMA</a>
                        </div>
                        
                        <div class="footer">
                            <p>© 2024 taalentio.com - CINEMA</p>
                            <p>Ceci est un email automatique, merci de ne pas y répondre.</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
        
        elif template_type == 'ai_talent_match':
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #4facfe; border-radius: 10px; margin-top: 20px; }}
                    .score {{ background: #f5f5f5; border: 2px dashed #4facfe; color: #4facfe; padding: 20px; 
                             text-align: center; border-radius: 10px; margin: 20px 0; font-weight: bold; }}
                    .opportunity-box {{ background: #f5f5f5; padding: 15px; border: 2px dashed #4facfe; 
                                       border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>🤖 Votre profil correspond à une opportunité !</h1>
                    </div>
                    <div class="content">
                        <h2>Bonjour {data.get('full_name', 'Utilisateur')},</h2>
                        <p>Notre intelligence artificielle a identifié que votre profil correspond à une recherche active :</p>
                        
                        <div class="opportunity-box">
                            <strong>Description de l'opportunité :</strong>
                            <p>{data.get('job_description', "Description de l'opportunité...")}</p>
                        </div>
                        
                        <div class="score">
                            <h2 style="margin: 0;">Score de correspondance : {data.get('match_score', 0)}%</h2>
                        </div>
                        
                        <p><strong>Raison du match :</strong></p>
                        <p>{data.get('match_reason', 'Votre profil correspond aux critères recherchés.')}</p>
                        
                        <div class="footer">
                            <p>© 2024 taalentio.com - AI Matching</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
        
        elif template_type == 'ai_cinema_match':
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #fa709a; border-radius: 10px; margin-top: 20px; }}
                    .score {{ background: #f5f5f5; border: 2px dashed #fa709a; color: #fa709a; padding: 20px; 
                             text-align: center; border-radius: 10px; margin: 20px 0; font-weight: bold; }}
                    .role-box {{ background: #f5f5f5; padding: 15px; border: 2px dashed #fa709a; 
                                border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>🎬 Votre profil correspond à un rôle cinéma !</h1>
                    </div>
                    <div class="content">
                        <h2>Bonjour {data.get('full_name', 'Utilisateur')},</h2>
                        <p>Excellente nouvelle ! Notre IA a détecté que votre profil CINEMA correspond à un casting en cours :</p>
                        
                        <div class="role-box">
                            <strong>Description du rôle :</strong>
                            <p>{data.get('role_description', "Description du rôle...")}</p>
                        </div>
                        
                        <div class="score">
                            <h2 style="margin: 0;">Score de correspondance : {data.get('match_score', 0)}%</h2>
                        </div>
                        
                        <p><strong>Pourquoi vous correspondez :</strong></p>
                        <p>{data.get('match_reason', 'Votre profil physique et vos compétences correspondent au rôle.')}</p>
                        
                        <div class="footer">
                            <p>© 2024 taalentio.com - CINEMA AI Matching</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
        
        elif template_type == 'project_selection':
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #a8edea; border-radius: 10px; margin-top: 20px; }}
                    .project-box {{ background: #f5f5f5; padding: 20px; border: 2px dashed #a8edea; 
                                   border-radius: 10px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>🎉 Vous avez été sélectionné pour un projet !</h1>
                    </div>
                    <div class="content">
                        <h2>Bonjour {data.get('full_name', 'Utilisateur')},</h2>
                        <p>Félicitations ! Vous avez été sélectionné pour participer au projet suivant :</p>
                        
                        <div class="project-box">
                            <h3 style="margin-top: 0; color: #a8edea;">📽️ {data.get('project_name', 'Nom du projet')}</h3>
                            <p><strong>Votre rôle :</strong> {data.get('role', 'Rôle à définir')}</p>
                        </div>
                        
                        <p>Un membre de l'équipe vous contactera prochainement pour les détails.</p>
                        
                        <div class="footer">
                            <p>© 2024 taalentio.com - Gestion de Projets</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
        
        elif template_type == 'login_credentials':
            login_url = f"https://{domain}/auth/login"
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #5b7ef5; border-radius: 10px; margin-top: 20px; }}
                    .button {{ display: inline-block; background: white; color: #5b7ef5; 
                              padding: 12px 30px; text-decoration: none; border: 2px solid #5b7ef5; 
                              border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .button:hover {{ background: #5b7ef5; color: white; }}
                    .credentials {{ background: #f5f5f5; border: 2px dashed #5b7ef5; padding: 20px; 
                                   border-radius: 5px; margin: 20px 0; }}
                    .credential-item {{ margin: 15px 0; }}
                    .credential-label {{ color: #666; font-size: 14px; font-weight: bold; }}
                    .credential-value {{ background: #fff; padding: 10px; border-radius: 3px; 
                                        font-family: monospace; font-size: 16px; margin-top: 5px; }}
                    .warning {{ background: #fff3cd; border: 2px dashed #ffc107; 
                               padding: 15px; margin: 20px 0; border-radius: 5px; }}
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
                        <h2>Bonjour {data.get('full_name', 'Utilisateur')},</h2>
                        <p>Voici vos identifiants de connexion pour accéder à votre espace personnel sur taalentio.com :</p>
                        
                        <div class="credentials">
                            <div class="credential-item">
                                <div class="credential-label">📧 Email OU Code unique</div>
                                <div class="credential-value">{data.get('email', 'email@example.com')} ou {data.get('unique_code', 'CODE123')}</div>
                            </div>
                            <div class="credential-item">
                                <div class="credential-label">🔒 Mot de passe temporaire</div>
                                <div class="credential-value">{data.get('password', 'MotDePasse123!')}</div>
                            </div>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Important :</strong> Changez votre mot de passe dès votre première connexion pour sécuriser votre compte.
                        </div>
                        
                        <div style="text-align: center;">
                            <a href="{login_url}" class="button">🔓 Se connecter</a>
                        </div>
                        
                        <div class="footer">
                            <p>© 2024 taalentio.com</p>
                            <p>Ceci est un email automatique, merci de ne pas y répondre.</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
        
        elif template_type == 'application_confirmation':
            profile_url = f"https://{domain}/profile/view/{data.get('unique_code', 'CODE123')}"
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #5b7ef5; border-radius: 10px; margin-top: 20px; }}
                    .button {{ display: inline-block; background: white; color: #5b7ef5; 
                              padding: 12px 30px; text-decoration: none; border: 2px solid #5b7ef5; 
                              border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .button:hover {{ background: #5b7ef5; color: white; }}
                    .code {{ background: #f5f5f5; border: 2px dashed #5b7ef5; padding: 15px; 
                            font-size: 24px; font-weight: bold; text-align: center; 
                            color: #5b7ef5; margin: 20px 0; border-radius: 5px; }}
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
                        <h2>Bonjour {data.get('full_name', 'Utilisateur')},</h2>
                        <p>Nous avons bien reçu votre candidature sur la plateforme taalentio.com !</p>
                        
                        <p>Votre profil de talent a été créé avec succès. Voici votre code unique :</p>
                        <div class="code">{data.get('unique_code', 'CODE123')}</div>
                        
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
        
        elif template_type == 'name_detection':
            profile_url = f"https://{domain}/profile/view/{data.get('unique_code', 'CODE123')}" if data.get('talent_type') == 'talent' else f"https://{domain}/cinema/view-talent/{data.get('unique_code', 'CODE123')}"
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #ff6b6b; border-radius: 10px; margin-top: 20px; }}
                    .alert {{ background: #fff3cd; border: 2px solid #ff6b6b; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .info-box {{ background: #f5f5f5; border-left: 4px solid #ff6b6b; padding: 15px; margin: 15px 0; }}
                    .button {{ display: inline-block; background: white; color: #ff6b6b; 
                              padding: 12px 30px; text-decoration: none; border: 2px solid #ff6b6b; 
                              border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .button:hover {{ background: #ff6b6b; color: white; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>🚨 Alerte : Nom Surveillé Détecté</h1>
                    </div>
                    <div class="content">
                        <div class="alert">
                            <h2 style="margin: 0; color: #ff6b6b;">⚠️ Nouvelle Inscription Détectée</h2>
                        </div>
                        
                        <p>Une personne dont le nom correspond à votre liste de surveillance vient de s'inscrire sur la plateforme.</p>
                        
                        <div class="info-box">
                            <strong>👤 Nom surveillé :</strong> {data.get('tracked_name', 'N/A')}<br>
                            <strong>📝 Nom enregistré :</strong> {data.get('registered_name', 'N/A')}<br>
                            <strong>🆔 Code unique :</strong> {data.get('unique_code', 'N/A')}<br>
                            <strong>🎭 Type :</strong> {data.get('talent_type_label', 'N/A')}<br>
                            <strong>📧 Email :</strong> {data.get('email', 'N/A')}<br>
                            <strong>🌍 Localisation :</strong> {data.get('city', 'N/A')}, {data.get('country', 'N/A')}
                        </div>
                        
                        <p><strong>Note de surveillance :</strong> {data.get('tracking_description', 'Aucune note')}</p>
                        
                        <div style="text-align: center;">
                            <a href="{profile_url}" class="button">👁️ Voir le profil complet</a>
                        </div>
                        
                        <p style="margin-top: 30px; font-size: 12px; color: #666;">
                            Cette notification a été envoyée automatiquement suite à la correspondance d'un nom dans votre liste de surveillance.
                        </p>
                    </div>
                    <div class="footer">
                        <p>© 2024 taalentio.com - Système de Surveillance</p>
                        <p>Ceci est un email automatique, merci de ne pas y répondre.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        else:
            return None
        
    def _log_email(self, recipient_email, recipient_name, subject, html_content, template_type, 
                   status='sent', error_message=None, sent_by_user_id=None, 
                   related_talent_code=None, related_project_id=None, related_cinema_talent_id=None):
        """Logger un email envoyé dans la base de données"""
        try:
            from app import db
            from app.models.email_log import EmailLog
            
            email_log = EmailLog(
                recipient_email=recipient_email,
                recipient_name=recipient_name,
                subject=subject,
                html_content=html_content,
                template_type=template_type,
                status=status,
                error_message=error_message,
                sent_by_user_id=sent_by_user_id,
                related_talent_code=related_talent_code,
                related_project_id=related_project_id,
                related_cinema_talent_id=related_cinema_talent_id
            )
            
            db.session.add(email_log)
            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.warning(f"Erreur lors du logging de l'email: {str(e)}")
            return False
    
    def send_email(self, to_email, subject, html_content, attachments=None, template_type='generic', 
                   recipient_name=None, sent_by_user_id=None, related_talent_code=None, 
                   related_project_id=None, related_cinema_talent_id=None):
        """
        Envoie un email via SendGrid avec logging
        
        Args:
            to_email: Email du destinataire
            subject: Sujet de l'email
            html_content: Contenu HTML de l'email
            attachments: Liste de dictionnaires avec 'content', 'filename', 'type'
            template_type: Type de template pour le logging
            recipient_name: Nom du destinataire
            sent_by_user_id: ID de l'utilisateur qui envoie
            related_talent_code: Code du talent lié
            related_project_id: ID du projet lié
            related_cinema_talent_id: ID du talent cinéma lié
        
        Returns:
            True si envoyé avec succès, False sinon
        """
        # Vérifier si ce type de template est activé
        from app.models.email_log import EmailLog
        if not EmailLog.is_template_enabled(template_type):
            print(f"⚠️  Email {template_type} désactivé, envoi annulé pour {to_email}")
            return False
        
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
            self._log_email(to_email, recipient_name, subject, html_content, template_type, 
                          status='failed', error_message=error_msg,
                          sent_by_user_id=sent_by_user_id, related_talent_code=related_talent_code,
                          related_project_id=related_project_id, related_cinema_talent_id=related_cinema_talent_id)
            return False
        
        if not from_email:
            error_msg = "❌ Email expéditeur manquant. Configurez SENDGRID_FROM_EMAIL"
            current_app.logger.error(error_msg)
            print(f"🔴 {error_msg}")
            self._log_email(to_email, recipient_name, subject, html_content, template_type, 
                          status='failed', error_message=error_msg,
                          sent_by_user_id=sent_by_user_id, related_talent_code=related_talent_code,
                          related_project_id=related_project_id, related_cinema_talent_id=related_cinema_talent_id)
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
                
                self._log_email(to_email, recipient_name, subject, html_content, template_type, 
                              status='sent', sent_by_user_id=sent_by_user_id,
                              related_talent_code=related_talent_code, related_project_id=related_project_id,
                              related_cinema_talent_id=related_cinema_talent_id)
                return True
            else:
                error_msg = f"❌ Erreur SendGrid - Code: {response.status_code}, Body: {response.body}"
                current_app.logger.error(error_msg)
                print(f"🔴 {error_msg}")
                
                self._log_email(to_email, recipient_name, subject, html_content, template_type, 
                              status='failed', error_message=error_msg,
                              sent_by_user_id=sent_by_user_id, related_talent_code=related_talent_code,
                              related_project_id=related_project_id, related_cinema_talent_id=related_cinema_talent_id)
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
            
            self._log_email(to_email, recipient_name, subject, html_content, template_type, 
                          status='failed', error_message=str(e),
                          sent_by_user_id=sent_by_user_id, related_talent_code=related_talent_code,
                          related_project_id=related_project_id, related_cinema_talent_id=related_cinema_talent_id)
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
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #5b7ef5; border-radius: 10px; margin-top: 20px; }}
                    .button {{ display: inline-block; background: white; color: #5b7ef5; 
                              padding: 12px 30px; text-decoration: none; border: 2px solid #5b7ef5; 
                              border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .button:hover {{ background: #5b7ef5; color: white; }}
                    .code {{ background: #f5f5f5; border: 2px dashed #5b7ef5; padding: 15px; 
                            font-size: 24px; font-weight: bold; text-align: center; 
                            color: #5b7ef5; margin: 20px 0; border-radius: 5px; }}
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
                attachments=attachments if attachments else None,
                template_type='application_confirmation',
                recipient_name=user.full_name,
                related_talent_code=user.unique_code
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
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #5b7ef5; border-radius: 10px; margin-top: 20px; }}
                    .button {{ display: inline-block; background: white; color: #5b7ef5; 
                              padding: 12px 30px; text-decoration: none; border: 2px solid #5b7ef5; 
                              border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .button:hover {{ background: #5b7ef5; color: white; }}
                    .credentials {{ background: #f5f5f5; border: 2px dashed #5b7ef5; padding: 20px; 
                                   border-radius: 5px; margin: 20px 0; }}
                    .credential-item {{ margin: 15px 0; }}
                    .credential-label {{ color: #666; font-size: 14px; font-weight: bold; }}
                    .credential-value {{ background: #fff; padding: 10px; border-radius: 3px; 
                                        font-family: monospace; font-size: 16px; margin-top: 5px; }}
                    .warning {{ background: #fff3cd; border: 2px dashed #ffc107; 
                               padding: 15px; margin: 20px 0; border-radius: 5px; }}
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
                                <div class="credential-label">📧 Identifiant (Code unique)</div>
                                <div class="credential-value">{user.unique_code}</div>
                            </div>
                            <div class="credential-item">
                                <div class="credential-label">🔒 Mot de passe</div>
                                <div class="credential-value">{password}</div>
                            </div>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Important :</strong> Ce mot de passe est temporaire. 
                            <strong>Nous vous recommandons vivement de le changer dès votre première connexion</strong> 
                            depuis votre profil pour sécuriser votre compte.
                        </div>
                        
                        <div style="text-align: center;">
                            <a href="{login_url}" class="button">🔓 Se connecter</a>
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
    
    def send_ai_match_notification(self, user, job_description, match_score, match_reason, sent_by_user_id=None):
        """
        Envoie une notification quand un profil match une recherche IA
        
        Args:
            user: Objet User dont le profil a matché
            job_description: Description du poste recherché
            match_score: Score de match (0-100)
            match_reason: Raison du match
            sent_by_user_id: ID de l'utilisateur qui a lancé la recherche
        
        Returns:
            True si envoyé, False sinon
        """
        try:
            domain = get_application_domain()
            profile_url = f"https://{domain}/profile/view/{user.unique_code}"
            
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
                    .match-badge {{ background: #10b981; color: white; padding: 10px 20px; 
                                    border-radius: 20px; display: inline-block; font-weight: bold; }}
                    .job-box {{ background: #fff; border: 2px solid #667eea; padding: 20px; 
                               border-radius: 5px; margin: 20px 0; }}
                    .button {{ display: inline-block; background: #667eea; color: white; 
                              padding: 12px 30px; text-decoration: none; border-radius: 5px; 
                              margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>🎯 Votre profil a matché une opportunité !</h1>
                    </div>
                    <div class="content">
                        <h2>Bonjour {user.full_name},</h2>
                        <p>Excellente nouvelle ! Notre système de matching intelligent a identifié votre profil comme 
                           particulièrement adapté pour l'opportunité suivante :</p>
                        
                        <div class="job-box">
                            <h3>Description de l'opportunité :</h3>
                            <p>{job_description[:500]}...</p>
                        </div>
                        
                        <p><strong>Score de correspondance :</strong> <span class="match-badge">{match_score}%</span></p>
                        
                        <p><strong>Pourquoi votre profil correspond :</strong></p>
                        <p>{match_reason}</p>
                        
                        <p>Nous vous encourageons à consulter votre profil et à le tenir à jour pour maximiser vos chances :</p>
                        <div style="text-align: center;">
                            <a href="{profile_url}" class="button">Voir mon profil</a>
                        </div>
                        
                        <p style="margin-top: 30px;">Bonne chance !<br>
                        <strong>L'équipe taalentio.com</strong></p>
                    </div>
                    <div class="footer">
                        <p>Cet email a été envoyé automatiquement suite à une recherche de talents par IA.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return self.send_email(
                to_email=user.email,
                subject=f"🎯 Votre profil correspond à une opportunité ({match_score}% de match)",
                html_content=html_content,
                template_type='ai_talent_match',
                recipient_name=user.full_name,
                sent_by_user_id=sent_by_user_id,
                related_talent_code=user.unique_code
            )
            
        except Exception as e:
            current_app.logger.error(f"Erreur envoi notification AI match: {str(e)}")
            return False
    
    def send_cinema_ai_match_notification(self, cinema_talent, role_description, match_score, match_reason, sent_by_user_id=None):
        """
        Envoie une notification quand un profil cinéma match une recherche IA
        
        Args:
            cinema_talent: Objet CinemaTalent dont le profil a matché
            role_description: Description du rôle recherché
            match_score: Score de match (0-100)
            match_reason: Raison du match
            sent_by_user_id: ID de l'utilisateur qui a lancé la recherche
        
        Returns:
            True si envoyé, False sinon
        """
        try:
            domain = get_application_domain()
            profile_url = f"https://{domain}/cinema/view-talent/{cinema_talent.unique_code}"
            
            logo_base64 = self._get_logo_base64()
            logo_img = f'<img src="data:image/png;base64,{logo_base64}" alt="taalentio.com" style="max-width: 250px; height: auto; margin-bottom: 15px;">' if logo_base64 else ''
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #fa709a; border-radius: 10px; margin-top: 20px; }}
                    .match-badge {{ background: #f5f5f5; color: #10b981; padding: 10px 20px; 
                                    border: 2px dashed #10b981; border-radius: 20px; display: inline-block; font-weight: bold; }}
                    .role-box {{ background: #f5f5f5; border: 2px dashed #fa709a; padding: 20px; 
                                border-radius: 5px; margin: 20px 0; }}
                    .button {{ display: inline-block; background: white; color: #fa709a; 
                              padding: 12px 30px; text-decoration: none; border: 2px solid #fa709a; 
                              border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .button:hover {{ background: #fa709a; color: white; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>🎬 Votre profil correspond à un rôle cinéma !</h1>
                    </div>
                    <div class="content">
                        <h2>Bonjour {cinema_talent.full_name},</h2>
                        <p>Excellente nouvelle ! Notre système de casting intelligent a identifié votre profil comme 
                           particulièrement adapté pour le rôle suivant :</p>
                        
                        <div class="role-box">
                            <h3>Description du rôle :</h3>
                            <p>{role_description[:500]}...</p>
                        </div>
                        
                        <p><strong>Score de correspondance :</strong> <span class="match-badge">{match_score}%</span></p>
                        
                        <p><strong>Pourquoi votre profil correspond :</strong></p>
                        <p>{match_reason}</p>
                        
                        <p>Consultez votre profil complet et assurez-vous qu'il est à jour :</p>
                        <div style="text-align: center;">
                            <a href="{profile_url}" class="button">Voir mon profil cinéma</a>
                        </div>
                        
                        <p style="margin-top: 30px;">Bonne chance pour votre casting !<br>
                        <strong>L'équipe taalentio.com</strong></p>
                    </div>
                    <div class="footer">
                        <p>Cet email a été envoyé automatiquement suite à une recherche de casting par IA.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return self.send_email(
                to_email=cinema_talent.email,
                subject=f"🎬 Votre profil correspond à un rôle cinéma ({match_score}% de match)",
                html_content=html_content,
                template_type='ai_cinema_match',
                recipient_name=cinema_talent.full_name,
                sent_by_user_id=sent_by_user_id,
                related_cinema_talent_id=cinema_talent.id
            )
            
        except Exception as e:
            current_app.logger.error(f"Erreur envoi notification cinema AI match: {str(e)}")
            return False
    
    def send_project_selection_confirmation(self, project_talent, sent_by_user_id=None):
        """
        Envoie un email de confirmation et félicitations pour la sélection dans un projet
        
        Args:
            project_talent: Objet ProjectTalent contenant les infos du talent et du projet
            sent_by_user_id: ID de l'utilisateur qui envoie l'email
        
        Returns:
            True si envoyé, False sinon
        """
        try:
            project = project_talent.project
            cinema_talent = project_talent.cinema_talent
            production = project.production
            
            domain = get_application_domain()
            profile_url = f"https://{domain}/cinema/view-talent/{cinema_talent.unique_code}"
            badge_url = f"https://{domain}/cinema/projects/talent/{project_talent.id}/generate-badge"
            
            logo_base64 = self._get_logo_base64()
            logo_img = f'<img src="data:image/png;base64,{logo_base64}" alt="taalentio.com" style="max-width: 250px; height: auto; margin-bottom: 15px;">' if logo_base64 else ''
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #10b981; border-radius: 10px; margin-top: 20px; }}
                    .success-box {{ background: #d1fae5; border: 2px dashed #10b981; 
                                   padding: 20px; margin: 20px 0; border-radius: 5px; }}
                    .project-info {{ background: #f5f5f5; border: 2px dashed #10b981; padding: 20px; 
                                    border-radius: 5px; margin: 20px 0; }}
                    .button {{ display: inline-block; background: white; color: #10b981; 
                              padding: 12px 30px; text-decoration: none; border: 2px solid #10b981; 
                              border-radius: 5px; margin: 10px 5px; font-weight: bold; }}
                    .button:hover {{ background: #10b981; color: white; }}
                    .production-contact {{ background: #fff3cd; border: 2px dashed #ffc107; 
                                         padding: 15px; margin: 20px 0; border-radius: 5px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>🎉 Félicitations ! Vous avez été sélectionné(e) !</h1>
                    </div>
                    <div class="content">
                        <h2>Bonjour {cinema_talent.full_name},</h2>
                        
                        <div class="success-box">
                            <h3>✨ Excellente nouvelle !</h3>
                            <p>Nous avons le plaisir de vous informer que vous avez été retenu(e) pour le projet suivant :</p>
                        </div>
                        
                        <div class="project-info">
                            <h3>📽️ {project.name}</h3>
                            <p><strong>Boîte de production :</strong> {production.name if production else 'N/A'}</p>
                            <p><strong>Type de talent :</strong> {project_talent.talent_type}</p>
                            {f'<p><strong>Rôle :</strong> {project_talent.role_description}</p>' if project_talent.role_description else ''}
                            <p><strong>Statut du projet :</strong> {project.get_status_display()}</p>
                        </div>
                        
                        <div class="production-contact">
                            <h4>📞 Prochaines étapes</h4>
                            <p>Veuillez contacter la production pour plus de détails sur le projet et les prochaines étapes :</p>
                            {f'<p><strong>Téléphone :</strong> {production.phone}</p>' if production and production.phone else ''}
                            {f'<p><strong>Email :</strong> {production.email}</p>' if production and production.email else ''}
                            {f'<p><strong>Adresse :</strong> {production.address}</p>' if production and production.address else ''}
                        </div>
                        
                        <p><strong>Votre profil et badge :</strong></p>
                        <div style="text-align: center;">
                            <a href="{profile_url}" class="button">Voir mon profil</a>
                            <a href="{badge_url}" class="button">Télécharger mon badge</a>
                        </div>
                        
                        <p style="margin-top: 30px;">Toute l'équipe vous félicite et vous souhaite beaucoup de succès dans ce projet !<br>
                        <strong>L'équipe taalentio.com</strong></p>
                    </div>
                    <div class="footer">
                        <p>Cet email a été envoyé automatiquement suite à votre sélection pour le projet.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return self.send_email(
                to_email=cinema_talent.email,
                subject=f"🎉 Félicitations ! Vous avez été sélectionné pour {project.name}",
                html_content=html_content,
                template_type='project_selection',
                recipient_name=cinema_talent.full_name,
                sent_by_user_id=sent_by_user_id,
                related_project_id=project.id,
                related_cinema_talent_id=cinema_talent.id
            )
            
        except Exception as e:
            current_app.logger.error(f"Erreur envoi confirmation sélection projet: {str(e)}")
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
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #10b981; border-radius: 10px; margin-top: 20px; }}
                    .success {{ background: #d1fae5; border: 2px dashed #10b981; 
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
    
    def send_weekly_admin_recap(self, admin_email, sent_by_user_id=None):
        """
        Envoie un récapitulatif hebdomadaire à l'admin avec toutes les nouvelles inscriptions
        Envoie 2 emails séparés : un pour les talents, un pour les talents cinéma
        
        Args:
            admin_email: Email de l'admin
            sent_by_user_id: ID de l'utilisateur qui envoie (optionnel)
        
        Returns:
            dict avec les résultats des envois
        """
        try:
            from app.models.user import User
            from app.models.cinema_talent import CinemaTalent
            from datetime import datetime, timedelta
            from sqlalchemy import and_
            
            # Calculer la période (derniers 7 jours)
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=7)
            
            # Récupérer les nouveaux talents
            new_talents = User.query.filter(
                and_(
                    User.created_at >= start_date,
                    User.created_at <= end_date,
                    User.role == 'user'
                )
            ).order_by(User.created_at.desc()).all()
            
            # Récupérer les nouveaux talents cinéma
            new_cinema_talents = CinemaTalent.query.filter(
                and_(
                    CinemaTalent.created_at >= start_date,
                    CinemaTalent.created_at <= end_date
                )
            ).order_by(CinemaTalent.created_at.desc()).all()
            
            results = {
                'talents_sent': False,
                'cinema_talents_sent': False,
                'talents_count': len(new_talents),
                'cinema_talents_count': len(new_cinema_talents)
            }
            
            domain = get_application_domain()
            logo_base64 = self._get_logo_base64()
            logo_img = f'<img src="data:image/png;base64,{logo_base64}" alt="taalentio.com" style="max-width: 250px; height: auto; margin-bottom: 15px;">' if logo_base64 else ''
            
            # Email pour les talents réguliers
            if new_talents:
                talents_html = self._build_recap_table(new_talents, domain, 'talent')
                
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                        .header {{ background: white; padding: 30px; text-align: center; }}
                        .content {{ background: white; padding: 30px; border: 2px dashed #4facfe; border-radius: 10px; margin-top: 20px; }}
                        .summary {{ background: #e3f2fd; border: 2px dashed #4facfe; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: center; }}
                        .talent-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                        .talent-table th {{ background: #f5f5f5; padding: 12px; border: 2px dashed #4facfe; text-align: left; font-weight: bold; }}
                        .talent-table td {{ padding: 12px; border: 1px solid #ddd; }}
                        .talent-table tr:hover {{ background: #f9f9f9; }}
                        .button {{ display: inline-block; background: white; color: #4facfe; padding: 8px 16px; 
                                  text-decoration: none; border: 2px solid #4facfe; border-radius: 5px; font-weight: bold; font-size: 12px; }}
                        .button:hover {{ background: #4facfe; color: white; }}
                        .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            {logo_img}
                            <h1>📊 Récapitulatif Hebdomadaire - Talents</h1>
                        </div>
                        <div class="content">
                            <div class="summary">
                                <h2 style="margin: 0; color: #4facfe;">✨ {len(new_talents)} Nouveau{'x' if len(new_talents) > 1 else ''} Talent{'s' if len(new_talents) > 1 else ''}</h2>
                                <p style="margin: 10px 0 0 0;">Période : {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}</p>
                            </div>
                            
                            <h3>Liste des nouvelles inscriptions :</h3>
                            {talents_html}
                            
                            <p style="margin-top: 30px;">Cordialement,<br>
                            <strong>Système taalentio.com</strong></p>
                        </div>
                        <div class="footer">
                            <p>Email automatique envoyé tous les dimanches</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                results['talents_sent'] = self.send_email(
                    to_email=admin_email,
                    subject=f"📊 Récapitulatif Hebdomadaire - {len(new_talents)} Nouveau{'x' if len(new_talents) > 1 else ''} Talent{'s' if len(new_talents) > 1 else ''}",
                    html_content=html_content,
                    template_type='weekly_recap_talents',
                    recipient_name='Admin',
                    sent_by_user_id=sent_by_user_id
                )
            
            # Email pour les talents cinéma
            if new_cinema_talents:
                cinema_html = self._build_recap_table(new_cinema_talents, domain, 'cinema')
                
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                        .header {{ background: white; padding: 30px; text-align: center; }}
                        .content {{ background: white; padding: 30px; border: 2px dashed #fa709a; border-radius: 10px; margin-top: 20px; }}
                        .summary {{ background: #ffe4e1; border: 2px dashed #fa709a; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: center; }}
                        .talent-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                        .talent-table th {{ background: #f5f5f5; padding: 12px; border: 2px dashed #fa709a; text-align: left; font-weight: bold; }}
                        .talent-table td {{ padding: 12px; border: 1px solid #ddd; }}
                        .talent-table tr:hover {{ background: #f9f9f9; }}
                        .button {{ display: inline-block; background: white; color: #fa709a; padding: 8px 16px; 
                                  text-decoration: none; border: 2px solid #fa709a; border-radius: 5px; font-weight: bold; font-size: 12px; }}
                        .button:hover {{ background: #fa709a; color: white; }}
                        .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            {logo_img}
                            <h1>🎬 Récapitulatif Hebdomadaire - Talents Cinéma</h1>
                        </div>
                        <div class="content">
                            <div class="summary">
                                <h2 style="margin: 0; color: #fa709a;">✨ {len(new_cinema_talents)} Nouveau{'x' if len(new_cinema_talents) > 1 else ''} Talent{'s' if len(new_cinema_talents) > 1 else ''} Cinéma</h2>
                                <p style="margin: 10px 0 0 0;">Période : {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}</p>
                            </div>
                            
                            <h3>Liste des nouvelles inscriptions :</h3>
                            {cinema_html}
                            
                            <p style="margin-top: 30px;">Cordialement,<br>
                            <strong>Système taalentio.com</strong></p>
                        </div>
                        <div class="footer">
                            <p>Email automatique envoyé tous les dimanches</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                results['cinema_talents_sent'] = self.send_email(
                    to_email=admin_email,
                    subject=f"🎬 Récapitulatif Hebdomadaire - {len(new_cinema_talents)} Nouveau{'x' if len(new_cinema_talents) > 1 else ''} Talent{'s' if len(new_cinema_talents) > 1 else ''} Cinéma",
                    html_content=html_content,
                    template_type='weekly_recap_cinema',
                    recipient_name='Admin',
                    sent_by_user_id=sent_by_user_id
                )
            
            return results
            
        except Exception as e:
            current_app.logger.error(f"Erreur envoi récapitulatif hebdomadaire: {str(e)}")
            import traceback
            current_app.logger.error(traceback.format_exc())
            return {'error': str(e)}
    
    def _build_recap_table(self, talents, domain, talent_type='talent'):
        """
        Construit le tableau HTML pour le récapitulatif
        
        Args:
            talents: Liste des talents (User ou CinemaTalent)
            domain: Domaine de l'application
            talent_type: 'talent' ou 'cinema'
        
        Returns:
            HTML du tableau
        """
        rows = []
        for talent in talents:
            if talent_type == 'talent':
                profile_url = f"https://{domain}/profile/view/{talent.unique_code}"
                city = talent.city or 'N/A'
                country = talent.country or 'N/A'
            else:
                profile_url = f"https://{domain}/cinema/view-talent/{talent.unique_code}"
                city = talent.city or 'N/A'
                country = talent.country or 'N/A'
            
            rows.append(f"""
                <tr>
                    <td><strong>{talent.full_name}</strong></td>
                    <td>{talent.unique_code}</td>
                    <td>{city}</td>
                    <td>{country}</td>
                    <td><a href="{profile_url}" class="button">Voir</a></td>
                </tr>
            """)
        
        return f"""
        <table class="talent-table">
            <thead>
                <tr>
                    <th>Nom Complet</th>
                    <th>Code Unique</th>
                    <th>Ville</th>
                    <th>Pays</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """
    
    def send_watchlist_notification(self, admin_email, talent_data, talent_type='talent'):
        """
        Envoie une notification à l'admin quand une personne de la watchlist s'inscrit
        
        Args:
            admin_email: Email de l'admin
            talent_data: Dictionnaire avec full_name, unique_code, city, country
            talent_type: 'talent' ou 'cinema'
        
        Returns:
            True si envoyé, False sinon
        """
        try:
            domain = get_application_domain()
            
            # Déterminer l'URL du profil
            if talent_type == 'talent':
                profile_url = f"https://{domain}/profile/view/{talent_data['unique_code']}"
                icon = "👤"
                type_label = "Talent"
                color = "#4facfe"
            else:
                profile_url = f"https://{domain}/cinema/view-talent/{talent_data['unique_code']}"
                icon = "🎬"
                type_label = "Talent Cinéma"
                color = "#fa709a"
            
            logo_base64 = self._get_logo_base64()
            logo_img = f'<img src="data:image/png;base64,{logo_base64}" alt="taalentio.com" style="max-width: 250px; height: auto; margin-bottom: 15px;">' if logo_base64 else ''
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed {color}; border-radius: 10px; margin-top: 20px; }}
                    .alert-box {{ background: #fff3cd; border: 2px dashed #ffc107; padding: 20px; 
                                 border-radius: 10px; margin: 20px 0; text-align: center; }}
                    .info-box {{ background: #f5f5f5; padding: 15px; border: 2px dashed {color}; 
                                border-radius: 5px; margin: 20px 0; }}
                    .button {{ display: inline-block; background: white; color: {color}; 
                              padding: 12px 30px; text-decoration: none; border: 2px solid {color}; 
                              border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .button:hover {{ background: {color}; color: white; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>🔔 Alerte - Liste de Surveillance</h1>
                    </div>
                    <div class="content">
                        <div class="alert-box">
                            <h2 style="margin: 0; color: #856404;">⚠️ Nouvelle inscription détectée !</h2>
                            <p style="margin: 10px 0 0 0;">Une personne de votre liste de surveillance s'est inscrite</p>
                        </div>
                        
                        <h3>{icon} Informations sur l'inscription :</h3>
                        <div class="info-box">
                            <p><strong>Type :</strong> {type_label}</p>
                            <p><strong>Nom Complet :</strong> {talent_data['full_name']}</p>
                            <p><strong>Code Unique :</strong> {talent_data['unique_code']}</p>
                            <p><strong>Ville :</strong> {talent_data.get('city', 'N/A')}</p>
                            <p><strong>Pays :</strong> {talent_data.get('country', 'N/A')}</p>
                        </div>
                        
                        <div style="text-align: center;">
                            <a href="{profile_url}" class="button">👁️ Voir le profil complet</a>
                        </div>
                        
                        <p style="margin-top: 30px; font-size: 12px; color: #666;">
                            Cette notification a été envoyée automatiquement parce que ce nom figure dans votre liste de surveillance.
                            Vous pouvez gérer votre liste dans les paramètres administrateur.
                        </p>
                    </div>
                    <div class="footer">
                        <p>© 2024 taalentio.com - Système de surveillance des inscriptions</p>
                        <p>Ceci est un email automatique, merci de ne pas y répondre.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return self.send_email(
                to_email=admin_email,
                subject=f"🔔 Alerte Watchlist - {talent_data['full_name']} s'est inscrit comme {type_label}",
                html_content=html_content,
                template_type='watchlist_notification',
                recipient_name='Admin',
                related_talent_code=talent_data['unique_code']
            )
            
        except Exception as e:
            current_app.logger.error(f"Erreur envoi notification watchlist: {str(e)}")
            return False
    
    def send_name_detection_notification(self, notification_email, tracked_name, match_data, sent_by_user_id=None):
        """
        Envoie une notification lors de la détection d'un nom surveillé
        
        Args:
            notification_email: Email où envoyer la notification
            tracked_name: Nom qui était surveillé
            match_data: Dictionnaire avec les informations de la correspondance
                - registered_name: Nom tel qu'enregistré
                - unique_code: Code unique du talent
                - talent_type: 'talent' ou 'cinema'
                - email: Email du talent
                - city: Ville
                - country: Pays
                - tracking_description: Note de surveillance
            sent_by_user_id: ID de l'utilisateur (optionnel)
        
        Returns:
            True si envoyé, False sinon
        """
        try:
            domain = get_application_domain()
            
            # Déterminer l'URL du profil et le label
            if match_data.get('talent_type') == 'talent':
                profile_url = f"https://{domain}/profile/view/{match_data['unique_code']}"
                talent_type_label = "Talent Standard"
            else:
                profile_url = f"https://{domain}/cinema/view-talent/{match_data['unique_code']}"
                talent_type_label = "Talent Cinéma"
            
            logo_base64 = self._get_logo_base64()
            logo_img = f'<img src="data:image/png;base64,{logo_base64}" alt="taalentio.com" style="max-width: 250px; height: auto; margin-bottom: 15px;">' if logo_base64 else ''
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: white; padding: 30px; text-align: center; }}
                    .content {{ background: white; padding: 30px; border: 2px dashed #ff6b6b; border-radius: 10px; margin-top: 20px; }}
                    .alert {{ background: #fff3cd; border: 2px solid #ff6b6b; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center; }}
                    .info-box {{ background: #f5f5f5; border-left: 4px solid #ff6b6b; padding: 15px; margin: 15px 0; }}
                    .button {{ display: inline-block; background: white; color: #ff6b6b; 
                              padding: 12px 30px; text-decoration: none; border: 2px solid #ff6b6b; 
                              border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .button:hover {{ background: #ff6b6b; color: white; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        {logo_img}
                        <h1>🚨 Alerte : Nom Surveillé Détecté</h1>
                    </div>
                    <div class="content">
                        <div class="alert">
                            <h2 style="margin: 0; color: #ff6b6b;">⚠️ Nouvelle Inscription Détectée</h2>
                        </div>
                        
                        <p>Une personne dont le nom correspond à votre liste de surveillance vient de s'inscrire sur la plateforme.</p>
                        
                        <div class="info-box">
                            <strong>👤 Nom surveillé :</strong> {tracked_name}<br>
                            <strong>📝 Nom enregistré :</strong> {match_data.get('registered_name', 'N/A')}<br>
                            <strong>🆔 Code unique :</strong> {match_data.get('unique_code', 'N/A')}<br>
                            <strong>🎭 Type :</strong> {talent_type_label}<br>
                            <strong>📧 Email :</strong> {match_data.get('email', 'N/A')}<br>
                            <strong>🌍 Localisation :</strong> {match_data.get('city', 'N/A')}, {match_data.get('country', 'N/A')}
                        </div>
                        
                        <p><strong>Note de surveillance :</strong> {match_data.get('tracking_description', 'Aucune note')}</p>
                        
                        <div style="text-align: center;">
                            <a href="{profile_url}" class="button">👁️ Voir le profil complet</a>
                        </div>
                        
                        <p style="margin-top: 30px; font-size: 12px; color: #666;">
                            Cette notification a été envoyée automatiquement suite à la correspondance d'un nom dans votre liste de surveillance.
                            Vous pouvez gérer votre liste dans les paramètres administrateur.
                        </p>
                    </div>
                    <div class="footer">
                        <p>© 2024 taalentio.com - Système de Surveillance</p>
                        <p>Ceci est un email automatique, merci de ne pas y répondre.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return self.send_email(
                to_email=notification_email,
                subject=f"🚨 Alerte Nom Surveillé - {match_data.get('registered_name', 'N/A')} vient de s'inscrire",
                html_content=html_content,
                template_type='name_detection',
                recipient_name='Admin',
                sent_by_user_id=sent_by_user_id,
                related_talent_code=match_data.get('unique_code')
            )
            
        except Exception as e:
            current_app.logger.error(f"Erreur envoi notification détection de nom: {str(e)}")
            return False

# Instance globale
email_service = EmailService()
