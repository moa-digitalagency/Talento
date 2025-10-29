"""
Service d'export des données des talents
Supporte Excel (XLSX), CSV, et PDF
"""
import os
import io
from datetime import datetime
from flask import current_app
import pandas as pd
import qrcode
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from app.utils.encryption import decrypt_sensitive_data
from config import Config

class ExportService:
    """Service d'export des données"""
    
    @staticmethod
    def _generate_qr_code_for_pdf(unique_code, profile_type='user', size=1.5):
        """
        Génère un QR code en mémoire pour le PDF avec la bonne URL
        
        Args:
            unique_code: Code unique du profil
            profile_type: 'user' ou 'cinema'
            size: Taille en inches
            
        Returns:
            Image object pour ReportLab ou None
        """
        try:
            # Obtenir l'URL de base correcte
            base_url = Config.get_base_url()
            
            # Construire l'URL du profil
            if profile_type == 'cinema':
                profile_url = f"{base_url}/cinema/profile/{unique_code}"
            else:
                profile_url = f"{base_url}/profile/view/{unique_code}"
            
            # Générer le QR code en mémoire
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(profile_url)
            qr.make(fit=True)
            
            # Créer l'image en mémoire
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convertir en bytes pour ReportLab
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Créer l'élément Image pour ReportLab
            return Image(img_buffer, width=size*inch, height=size*inch)
        except Exception as e:
            print(f"Erreur génération QR code PDF: {e}")
            return None
    
    @staticmethod
    def export_to_excel(users, filename='talents_export.xlsx'):
        """
        Exporter la liste des talents vers Excel
        
        Args:
            users: Liste d'objets User
            filename: Nom du fichier de sortie
            
        Returns:
            bytes: Données du fichier Excel
        """
        data = []
        
        for user in users:
            talents_names = [ut.talent.name for ut in user.talents] if user.talents else []
            
            data.append({
                'Code Unique': user.formatted_code,
                'Prénom': user.first_name,
                'Nom': user.last_name,
                'Email': user.email,
                'Téléphone': user.phone or 'N/A',
                'WhatsApp': user.whatsapp or 'N/A',
                'Pays d\'origine': user.country.name if user.country else 'N/A',
                'Nationalité': user.nationality if user.nationality else 'N/A',
                'Pays de résidence': user.residence_country.name if user.residence_country else 'N/A',
                'Ville de résidence': user.residence_city.name if user.residence_city else 'N/A',
                'Genre': user.gender or 'N/A',
                'Talents': ', '.join(talents_names),
                'Disponibilité': user.availability or 'N/A',
                'Mode de travail': user.work_mode or 'N/A',
                'Score Profil': user.profile_score or 0,
                'CV': 'Oui' if user.cv_filename else 'Non',
                'Portfolio': 'Oui' if user.portfolio_url else 'Non',
                'Date d\'inscription': user.created_at.strftime('%d/%m/%Y') if user.created_at else 'N/A',
            })
        
        df = pd.DataFrame(data)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Talents', index=False)
            
            worksheet = writer.sheets['Talents']
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
        
        output.seek(0)
        return output.getvalue()
    
    @staticmethod
    def export_to_csv(users, filename='talents_export.csv'):
        """
        Exporter la liste des talents vers CSV
        
        Args:
            users: Liste d'objets User
            filename: Nom du fichier de sortie
            
        Returns:
            str: Données CSV
        """
        data = []
        
        for user in users:
            talents_names = [ut.talent.name for ut in user.talents] if user.talents else []
            
            data.append({
                'Code Unique': user.formatted_code,
                'Prénom': user.first_name,
                'Nom': user.last_name,
                'Email': user.email,
                'Téléphone': user.phone or 'N/A',
                'WhatsApp': user.whatsapp or 'N/A',
                'Pays d\'origine': user.country.name if user.country else 'N/A',
                'Nationalité': user.nationality if user.nationality else 'N/A',
                'Pays de résidence': user.residence_country.name if user.residence_country else 'N/A',
                'Ville de résidence': user.residence_city.name if user.residence_city else 'N/A',
                'Genre': user.gender or 'N/A',
                'Talents': '; '.join(talents_names),
                'Disponibilité': user.availability or 'N/A',
                'Mode de travail': user.work_mode or 'N/A',
                'Score Profil': user.profile_score or 0,
                'CV': 'Oui' if user.cv_filename else 'Non',
                'Portfolio': 'Oui' if user.portfolio_url else 'Non',
                'Date Inscription': user.created_at.strftime('%d/%m/%Y') if user.created_at else 'N/A',
            })
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False)
    
    @staticmethod
    def export_list_to_pdf(users, filename='talents_list.pdf', current_user=None):
        """
        Exporter la liste des talents vers PDF (format tableau paysage)
        
        Args:
            users: Liste d'objets User
            filename: Nom du fichier de sortie
            current_user: Utilisateur qui télécharge le document
            
        Returns:
            bytes: Données du fichier PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Ajout du logo
        logo_path = os.path.join('app', 'static', 'img', 'logo-full.png')
        if not os.path.exists(logo_path):
            logo_path = os.path.join('static', 'img', 'logo-full.png')
        
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=2.5*inch, height=1*inch, kind='proportional')
                logo.hAlign = 'CENTER'
                elements.append(logo)
                elements.append(Spacer(1, 10))
            except:
                pass
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4F46E5'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph("Liste de Talent", title_style))
        elements.append(Spacer(1, 15))
        
        data = [['Code', 'Nom Complet', 'Talents', 'Pays Origine', 'Ville Résidence', 'Téléphone', 'WhatsApp']]
        
        cell_style = ParagraphStyle(
            'CellStyle',
            parent=styles['Normal'],
            fontSize=7,
            leading=9,
            alignment=TA_LEFT
        )
        
        for user in users:
            talents_names = [ut.talent.name for ut in user.talents] if user.talents else []
            talents_str = ', '.join(talents_names) if talents_names else 'N/A'
            
            data.append([
                user.formatted_code,
                f"{user.first_name} {user.last_name}",
                Paragraph(talents_str, cell_style),
                user.country.name if user.country else 'N/A',
                user.residence_city.name if user.residence_city else 'N/A',
                user.phone if user.phone else 'N/A',
                user.whatsapp if user.whatsapp else 'N/A'
            ])
        
        table = Table(data, colWidths=[1.2*inch, 1.8*inch, 2*inch, 1.3*inch, 1.3*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6B7280'),
            alignment=TA_LEFT
        )
        
        footer_text = f"Date: {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
        if current_user:
            footer_text += f" | Téléchargé par: {current_user.first_name} {current_user.last_name} ({current_user.formatted_code})"
        
        elements.append(Paragraph(footer_text, footer_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    @staticmethod
    def export_talent_card_pdf(user):
        """
        Générer une fiche talent individuelle en PDF avec design professionnel
        
        Args:
            user: Objet User
            
        Returns:
            bytes: Données du fichier PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Couleurs de la plateforme
        color_blue = colors.HexColor('#3B82F6')
        color_purple = colors.HexColor('#9333EA')
        color_cyan = colors.HexColor('#06B6D4')
        color_indigo = colors.HexColor('#4F46E5')
        color_gray = colors.HexColor('#6B7280')
        
        # ==== EN-TÊTE AVEC LOGO ET TITRE ====
        header_style = ParagraphStyle(
            'Header',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=color_indigo,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=5
        )
        
        subtitle_header_style = ParagraphStyle(
            'SubtitleHeader',
            parent=styles['Normal'],
            fontSize=12,
            textColor=color_gray,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        # Ajout du logo
        logo_path = os.path.join('static', 'img', 'logo-full.png')
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=2.5*inch, height=1*inch, kind='proportional')
                logo.hAlign = 'CENTER'
                elements.append(logo)
                elements.append(Spacer(1, 10))
            except:
                pass
        
        elements.append(Paragraph("Plateforme de Centralisation des Talents Africain Subsahrien aux Maroc", subtitle_header_style))
        
        # Ligne de séparation
        line_table = Table([['']],  colWidths=[6.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 3, color_indigo),
            ('LINEBELOW', (0, 0), (-1, 0), 1, color_cyan),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 15))
        
        # ==== SECTION PRINCIPALE: PHOTO, INFO & QR CODE ====
        def get_initial(name):
            """Extraire l'initiale de manière sécurisée"""
            if not name:
                return '?'
            clean_name = str(name).strip()
            return clean_name[0].upper() if clean_name else '?'
        
        first_initial = get_initial(user.first_name)
        last_initial = get_initial(user.last_name)
        initials = f"{first_initial}{last_initial}"
        
        # Générer la photo ou le placeholder basé sur le genre
        photo_element = None
        if user.photo_filename:
            try:
                photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos', user.photo_filename)
                if os.path.exists(photo_path):
                    photo_element = Image(photo_path, width=1.8*inch, height=1.8*inch)
            except:
                pass
        
        if not photo_element:
            # Placeholder avec initiales
            placeholder_color = color_blue if user.gender == 'M' else (color_purple if user.gender == 'F' else color_cyan)
            
            placeholder_style = ParagraphStyle(
                'Placeholder',
                parent=styles['Normal'],
                fontSize=60,
                textColor=colors.white,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                leading=72
            )
            
            # Créer une table pour le placeholder avec fond coloré
            placeholder_table = Table([[Paragraph(initials, placeholder_style)]], colWidths=[1.8*inch], rowHeights=[1.8*inch])
            placeholder_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), placeholder_color),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, -1), 2, colors.white),
            ]))
            photo_element = placeholder_table
        
        # Informations principales dans une carte
        info_name_style = ParagraphStyle(
            'InfoName',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=color_indigo,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=5
        )
        
        info_code_style = ParagraphStyle(
            'InfoCode',
            parent=styles['Normal'],
            fontSize=14,
            textColor=color_gray,
            alignment=TA_CENTER,
            fontName='Courier-Bold',
            spaceAfter=10
        )
        
        # Créer une sous-table pour les informations nom et code
        info_data_main = [
            [Paragraph(f"{user.first_name} {user.last_name}", info_name_style)],
            [Paragraph(f"Code: {user.formatted_code}", info_code_style)],
        ]
        info_table_main = Table(info_data_main, colWidths=[2.5*inch])
        info_table_main.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        # QR Code - généré à la volée avec la bonne URL
        qr_element = ExportService._generate_qr_code_for_pdf(user.unique_code, profile_type='user', size=1.5)
        
        # Placeholder simple pour QR code si la génération échoue
        if not qr_element:
            qr_placeholder_style = ParagraphStyle(
                'QRPlaceholder', 
                parent=styles['Normal'], 
                fontSize=10, 
                alignment=TA_CENTER, 
                textColor=colors.white,
                leading=12
            )
            
            # Créer un placeholder gris pour le QR code
            qr_placeholder_table = Table([[Paragraph("QR Code", qr_placeholder_style)]], colWidths=[1.5*inch], rowHeights=[1.5*inch])
            qr_placeholder_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), color_gray),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, -1), 2, colors.white),
            ]))
            qr_element = qr_placeholder_table
        
        # Table principale avec photo, info et QR
        main_table = Table(
            [[photo_element, info_table_main, qr_element]], 
            colWidths=[2*inch, 2.5*inch, 2*inch]
        )
        main_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('ALIGN', (2, 0), (2, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F3F4F6')),
            ('BOX', (0, 0), (-1, -1), 2, color_indigo),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(main_table)
        elements.append(Spacer(1, 20))
        
        # ==== SECTION IDENTITÉ ====
        section_style = ParagraphStyle(
            'Section',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            leftIndent=10
        )
        
        # Titre de section
        identity_title = Table([['IDENTITÉ']], colWidths=[6.5*inch])
        identity_title.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), color_blue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(identity_title)
        
        # Style pour le contenu avec text wrapping
        content_style = ParagraphStyle(
            'ContentStyle',
            parent=styles['Normal'],
            fontSize=10,
            leading=12,
            alignment=TA_LEFT
        )
        
        # Parser les langues si c'est du JSON
        languages_display = 'Information non disponible'
        if user.languages:
            try:
                import json
                if user.languages.startswith('['):
                    languages_list = json.loads(user.languages)
                    languages_display = ', '.join(languages_list)
                else:
                    languages_display = user.languages
            except:
                languages_display = user.languages
        
        info_data = [
            ['Email', user.email or 'Information non disponible'],
            ['Téléphone', user.phone or 'Information non disponible'],
            ['WhatsApp', user.whatsapp or 'Information non disponible'],
            ['Adresse', user.address or 'Information non disponible'],
            ['Passeport', (user.passport_number.upper() if user.passport_number else 'Non renseigné')],
            ['Carte de séjour', (user.residence_card.upper() if user.residence_card else 'Non renseigné')],
            ['Date de naissance', (user.date_of_birth.strftime('%d/%m/%Y') + (f' ({user.age} ans)' if user.age else '')) if user.date_of_birth else 'Information non disponible'],
            ['Genre', {'M': 'Masculin', 'F': 'Féminin', 'N': 'Non précisé'}.get(user.gender, 'Information non disponible')],
            ['Pays d\'origine', user.country.name if user.country else 'Information non disponible'],
            ['Nationalité', user.nationality if user.nationality else 'Information non disponible'],
            ['Pays de résidence', user.residence_country.name if user.residence_country else 'Information non disponible'],
            ['Ville de résidence', user.residence_city.name if user.residence_city else 'Information non disponible'],
            ['Langues', Paragraph(languages_display, content_style)],
            ['Années d\'expérience', str(user.years_experience) + ' ans' if user.years_experience else 'Information non disponible'],
            ['Éducation', Paragraph(user.education or 'Information non disponible', content_style)],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4.5*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#DBEAFE')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, color_gray),
            ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 15))
        
        # ==== SECTION TALENTS & COMPÉTENCES ====
        if user.talents:
            elements.append(PageBreak())
            talents_title = Table([['TALENTS & COMPÉTENCES']], colWidths=[6.5*inch])
            talents_title.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), color_purple),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(talents_title)
            
            talents_by_category = {}
            for ut in user.talents:
                category = ut.talent.category
                if category not in talents_by_category:
                    talents_by_category[category] = []
                talents_by_category[category].append(ut.talent.name)
            
            talents_data = []
            for category, talents in talents_by_category.items():
                talents_data.append([category, ', '.join(talents)])
            
            talents_table = Table(talents_data, colWidths=[2*inch, 4.5*inch])
            talents_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3E8FF')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, color_gray),
                ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
            ]))
            elements.append(talents_table)
            elements.append(Spacer(1, 15))
        
        # ==== SECTION PROFIL PROFESSIONNEL ====
        prof_title = Table([['PROFIL PROFESSIONNEL']], colWidths=[6.5*inch])
        prof_title.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), color_cyan),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(prof_title)
        
        prof_data = [
            ['Disponibilité', user.availability or 'Information non disponible'],
            ['Mode de travail', user.work_mode or 'Information non disponible'],
            ['Fourchette tarifaire', user.rate_range or 'Information non disponible'],
            ['Score de profil', f"{user.profile_score or 0}/100"],
            ['CV disponible', 'Oui' if user.cv_filename else 'Non'],
            ['Portfolio', user.portfolio_url if user.portfolio_url else 'Information non disponible'],
            ['Date d\'inscription', user.created_at.strftime('%d/%m/%Y') if user.created_at else 'Information non disponible'],
        ]
        
        prof_table = Table(prof_data, colWidths=[2*inch, 4.5*inch])
        prof_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#CFFAFE')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, color_gray),
            ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
        ]))
        elements.append(prof_table)
        elements.append(Spacer(1, 15))
        
        # ==== SECTION BIOGRAPHIE ====
        if user.bio:
            bio_title = Table([['BIOGRAPHIE']], colWidths=[6.5*inch])
            bio_title.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#10B981')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(bio_title)
            
            bio_style = ParagraphStyle(
                'Bio',
                parent=styles['Normal'],
                fontSize=10,
                leading=14,
                alignment=TA_JUSTIFY
            )
            
            bio_table = Table([[Paragraph(user.bio, bio_style)]], colWidths=[6.5*inch])
            bio_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0FDF4')),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BOX', (0, 0), (-1, -1), 0.5, color_gray),
            ]))
            elements.append(bio_table)
            elements.append(Spacer(1, 15))
        
        # ==== SECTION RÉSEAUX SOCIAUX ====
        # Collecter uniquement les réseaux sociaux remplis
        social_links = []
        social_platforms = {
            'LinkedIn': 'linkedin',
            'Instagram': 'instagram', 
            'Twitter': 'twitter',
            'Facebook': 'facebook',
            'TikTok': 'tiktok',
            'YouTube': 'youtube',
            'GitHub': 'github',
            'Behance': 'behance',
            'Dribbble': 'dribbble',
            'Pinterest': 'pinterest',
            'Snapchat': 'snapchat',
            'Telegram': 'telegram'
        }
        
        for display_name, platform in social_platforms.items():
            value = getattr(user, platform, None)
            if value:  # N'ajouter que si la valeur existe
                social_links.append([display_name, value])
        
        # N'afficher la section que s'il y a au moins un réseau social rempli
        if social_links:
            social_title = Table([['RÉSEAUX SOCIAUX']], colWidths=[6.5*inch])
            social_title.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EC4899')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(social_title)
            
            social_table = Table(social_links, colWidths=[2*inch, 4.5*inch])
            social_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FCE7F3')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 0.5, color_gray),
                ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
            ]))
            elements.append(social_table)
            elements.append(Spacer(1, 15))
        
        # ==== FOOTER ====
        elements.append(Spacer(1, 20))
        footer_line = Table([['']],  colWidths=[6.5*inch])
        footer_line.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, color_indigo),
        ]))
        elements.append(footer_line)
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=color_gray,
            alignment=TA_CENTER
        )
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", footer_style))
        elements.append(Paragraph("Plateforme Talento CINEMA - Talents du Cinéma Africain", footer_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    @staticmethod
    def export_cinema_talent_card_pdf(cinema_talent):
        """
        Générer une fiche talent CINEMA individuelle en PDF
        
        Args:
            cinema_talent: Objet CinemaTalent
            
        Returns:
            bytes: Données du fichier PDF
        """
        from app.models import Country
        from app.data.world_countries import NATIONALITIES_WITH_FLAGS
        import json
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Couleurs de la plateforme
        color_blue = colors.HexColor('#3B82F6')
        color_purple = colors.HexColor('#9333EA')
        color_green = colors.HexColor('#22c55e')
        color_indigo = colors.HexColor('#4F46E5')
        color_gray = colors.HexColor('#6B7280')
        
        # ==== EN-TÊTE ====
        platform_style = ParagraphStyle(
            'Platform',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=color_indigo,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=8
        )
        
        header_style = ParagraphStyle(
            'Header',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=color_purple,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=6
        )
        
        subtitle_header_style = ParagraphStyle(
            'SubtitleHeader',
            parent=styles['Normal'],
            fontSize=12,
            textColor=color_gray,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        # Ajout du logo
        logo_path = os.path.join('static', 'img', 'logo-full.png')
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=2.5*inch, height=1*inch, kind='proportional')
                logo.hAlign = 'CENTER'
                elements.append(logo)
                elements.append(Spacer(1, 10))
            except:
                pass
        
        elements.append(Paragraph("CINEMA - FICHE DE TALENT", header_style))
        elements.append(Paragraph("Profil Cinématographique - Talents du Cinéma Africain", subtitle_header_style))
        
        # Ligne de séparation
        line_table = Table([['']],  colWidths=[6.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 3, color_indigo),
            ('LINEBELOW', (0, 0), (-1, 0), 1, color_green),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 15))
        
        # ==== SECTION PRINCIPALE: PHOTO, INFO & QR CODE ====
        def get_initial(name):
            """Extraire l'initiale de manière sécurisée"""
            if not name:
                return '?'
            clean_name = str(name).strip()
            return clean_name[0].upper() if clean_name else '?'
        
        first_initial = get_initial(cinema_talent.first_name)
        last_initial = get_initial(cinema_talent.last_name)
        initials = f"{first_initial}{last_initial}"
        
        # Générer la photo ou le placeholder
        photo_element = None
        if cinema_talent.id_photo_filename:
            try:
                photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos', cinema_talent.id_photo_filename)
                if os.path.exists(photo_path):
                    photo_element = Image(photo_path, width=1.8*inch, height=1.8*inch)
            except:
                pass
        
        if not photo_element:
            # Placeholder avec initiales
            placeholder_color = color_blue if cinema_talent.gender == 'M' else (color_purple if cinema_talent.gender == 'F' else color_green)
            
            placeholder_style = ParagraphStyle(
                'Placeholder',
                parent=styles['Normal'],
                fontSize=60,
                textColor=colors.white,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                leading=72
            )
            
            placeholder_table = Table([[Paragraph(initials, placeholder_style)]], colWidths=[1.8*inch], rowHeights=[1.8*inch])
            placeholder_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), placeholder_color),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, -1), 2, colors.white),
            ]))
            photo_element = placeholder_table
        
        # QR Code - généré à la volée avec la bonne URL
        qr_element = ExportService._generate_qr_code_for_pdf(cinema_talent.unique_code, profile_type='cinema', size=1.5)
        
        # Colonne centrale: Nom, date de naissance, genre
        full_name = f"{cinema_talent.first_name} {cinema_talent.last_name}"
        
        # Calculer la date de naissance formatée et l'âge
        birth_date_str = 'Non renseignée'
        age_display = ''
        if cinema_talent.date_of_birth:
            birth_date_str = cinema_talent.date_of_birth.strftime('%d/%m/%Y')
            from datetime import date
            today = date.today()
            age = today.year - cinema_talent.date_of_birth.year - ((today.month, today.day) < (cinema_talent.date_of_birth.month, cinema_talent.date_of_birth.day))
            age_display = f" ({age} ans)"
        
        gender_str = {'M': 'Homme', 'F': 'Femme', 'N': 'Non précisé'}.get(cinema_talent.gender, 'Non renseigné')
        
        # Styles pour la colonne centrale
        name_style = ParagraphStyle(
            'Name',
            parent=styles['Normal'],
            fontSize=16,
            textColor=color_indigo,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            leading=18
        )
        
        info_style = ParagraphStyle(
            'InfoCenter',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#374151'),
            fontName='Helvetica',
            alignment=TA_CENTER,
            leading=14
        )
        
        # Créer la colonne centrale avec nom sur 2 lignes, date et genre
        name_parts = full_name.upper().split(' ', 1)
        if len(name_parts) == 2:
            name_text = f"{name_parts[0]}<br/>{name_parts[1]}"
        else:
            name_text = name_parts[0]
        
        center_content = [
            [Paragraph(name_text, name_style)],
            [Paragraph(f"<b>Né(e) le:</b> {birth_date_str}{age_display}", info_style)],
            [Paragraph(f"<b>Genre:</b> {gender_str}", info_style)],
            [Paragraph(f"<b>Code:</b> {cinema_talent.unique_code}", info_style)]
        ]
        
        center_table = Table(center_content, colWidths=[2.5*inch])
        center_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        # Layout de la section principale
        if qr_element:
            main_layout = Table([[photo_element, center_table, qr_element]], colWidths=[2*inch, 2.5*inch, 2*inch])
        else:
            main_layout = Table([[photo_element, center_table]], colWidths=[2*inch, 4.5*inch])
        
        main_layout.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(main_layout)
        elements.append(Spacer(1, 20))
        
        # ==== SECTION IDENTITÉ ====
        identity_title = Table([['IDENTITÉ & CONTACT']], colWidths=[6.5*inch])
        identity_title.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), color_blue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(identity_title)
        
        # Calcul de l'âge
        age_str = 'Non renseigné'
        if cinema_talent.date_of_birth:
            from datetime import date
            today = date.today()
            age = today.year - cinema_talent.date_of_birth.year - ((today.month, today.day) < (cinema_talent.date_of_birth.month, cinema_talent.date_of_birth.day))
            age_str = f"{age} ans"
        
        # Récupérer les drapeaux
        country_origin = Country.query.filter_by(name=cinema_talent.country_of_origin).first() if cinema_talent.country_of_origin else None
        country_residence = Country.query.filter_by(name=cinema_talent.country_of_residence).first() if cinema_talent.country_of_residence else None
        
        flag_origin = country_origin.flag if country_origin else ''
        flag_residence = country_residence.flag if country_residence else ''
        flag_nationality = ''
        if cinema_talent.nationality:
            for item in NATIONALITIES_WITH_FLAGS:
                if item['nationality'] == cinema_talent.nationality:
                    flag_nationality = item['flag']
                    break
        
        # Déchiffrer le téléphone, WhatsApp et le numéro de pièce d'identité
        phone_decrypted = 'Non renseigné'
        if cinema_talent.phone_encrypted:
            try:
                phone_decrypted = decrypt_sensitive_data(cinema_talent.phone_encrypted)
            except:
                phone_decrypted = 'Non disponible'
        
        whatsapp_decrypted = 'Non renseigné'
        if cinema_talent.whatsapp_encrypted:
            try:
                whatsapp_decrypted = decrypt_sensitive_data(cinema_talent.whatsapp_encrypted)
            except:
                whatsapp_decrypted = 'Non disponible'
        
        id_document_number = 'Non renseigné'
        id_document_label = 'Non renseigné'
        if cinema_talent.id_document_number_encrypted:
            try:
                id_document_number = decrypt_sensitive_data(cinema_talent.id_document_number_encrypted)
            except:
                id_document_number = 'Non disponible'
        
        if cinema_talent.id_document_type == 'passport':
            id_document_label = 'Passeport'
        elif cinema_talent.id_document_type == 'national_id':
            id_document_label = 'Carte d\'identité nationale'
        elif cinema_talent.id_document_type == 'residence_permit':
            id_document_label = 'Titre de séjour'
        
        info_data = [
            ['Pièce d\'identité', f"{id_document_label} - {id_document_number}" if cinema_talent.id_document_type else 'Non renseigné'],
            ['Email', cinema_talent.email or 'Non renseigné'],
            ['Téléphone', phone_decrypted],
            ['WhatsApp', whatsapp_decrypted],
            ['Site Web', cinema_talent.website or 'Non renseigné'],
            ['Pays d\'origine', f"{flag_origin} {cinema_talent.country_of_origin}" if cinema_talent.country_of_origin else 'Non renseigné'],
            ['Nationalité', f"{flag_nationality} {cinema_talent.nationality}" if cinema_talent.nationality else 'Non renseigné'],
            ['Résidence', f"{cinema_talent.city_of_residence}, {flag_residence} {cinema_talent.country_of_residence}" if cinema_talent.country_of_residence else 'Non renseigné'],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4.5*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#DBEAFE')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, color_gray),
            ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 15))
        
        # ==== ORIGINES ====
        try:
            ethnicities = json.loads(cinema_talent.ethnicities) if cinema_talent.ethnicities else []
        except:
            ethnicities = []
        
        if ethnicities:
            origins_title = Table([['ORIGINES']], colWidths=[6.5*inch])
            origins_title.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), color_green),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(origins_title)
            
            origins_data = [['Ethnicités', ', '.join(ethnicities)]]
            origins_table = Table(origins_data, colWidths=[2*inch, 4.5*inch])
            origins_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#DCFCE7')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 0.5, color_gray),
            ]))
            elements.append(origins_table)
            elements.append(Spacer(1, 15))
        
        # ==== LANGUES ====
        try:
            languages = json.loads(cinema_talent.languages) if cinema_talent.languages else []
        except:
            languages = []
        
        if languages:
            lang_title = Table([['LANGUES PARLÉES']], colWidths=[6.5*inch])
            lang_title.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#06B6D4')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(lang_title)
            
            lang_text = ', '.join(languages)
            lang_para = Paragraph(lang_text, styles['Normal'])
            lang_table = Table([[lang_para]], colWidths=[6.5*inch])
            lang_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#CFFAFE')),
                ('BOX', (0, 0), (-1, -1), 0.5, color_gray),
            ]))
            elements.append(lang_table)
            elements.append(Spacer(1, 15))
        
        # ==== CARACTÉRISTIQUES PHYSIQUES ====
        has_physical = (cinema_talent.height or cinema_talent.eye_color or cinema_talent.hair_color or 
                       cinema_talent.hair_type or cinema_talent.skin_tone or cinema_talent.build)
        
        if has_physical:
            phys_title = Table([['CARACTÉRISTIQUES PHYSIQUES']], colWidths=[6.5*inch])
            phys_title.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F97316')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(phys_title)
            
            phys_data = []
            if cinema_talent.height:
                phys_data.append(['Taille', f"{cinema_talent.height} cm"])
            if cinema_talent.eye_color:
                phys_data.append(['Couleur des yeux', cinema_talent.eye_color])
            if cinema_talent.hair_color:
                phys_data.append(['Couleur de cheveux', cinema_talent.hair_color])
            if cinema_talent.hair_type:
                phys_data.append(['Type de cheveux', cinema_talent.hair_type])
            if cinema_talent.skin_tone:
                phys_data.append(['Teint', cinema_talent.skin_tone])
            if cinema_talent.build:
                phys_data.append(['Corpulence', cinema_talent.build])
            
            phys_table = Table(phys_data, colWidths=[2*inch, 4.5*inch])
            phys_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FFEDD5')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, color_gray),
                ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
            ]))
            elements.append(phys_table)
            elements.append(Spacer(1, 15))
        
        # ==== TYPES DE TALENTS ====
        try:
            talent_types = json.loads(cinema_talent.talent_types) if cinema_talent.talent_types else []
        except:
            talent_types = []
        
        if talent_types:
            talents_title = Table([['TYPES DE TALENTS']], colWidths=[6.5*inch])
            talents_title.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EAB308')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(talents_title)
            
            talents_text = ', '.join(talent_types)
            talents_para = Paragraph(talents_text, styles['Normal'])
            talents_data = [[talents_para]]
            talents_table = Table(talents_data, colWidths=[6.5*inch])
            talents_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF9C3')),
                ('BOX', (0, 0), (-1, -1), 0.5, color_gray),
            ]))
            elements.append(talents_table)
            elements.append(Spacer(1, 15))
        
        # ==== COMPÉTENCES ARTISTIQUES ====
        try:
            other_talents = json.loads(cinema_talent.other_talents) if cinema_talent.other_talents else []
        except:
            other_talents = []
        
        if other_talents:
            comp_title = Table([['COMPÉTENCES ARTISTIQUES']], colWidths=[6.5*inch])
            comp_title.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EC4899')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(comp_title)
            
            comp_text = ', '.join(other_talents)
            comp_para = Paragraph(comp_text, styles['Normal'])
            comp_table = Table([[comp_para]], colWidths=[6.5*inch])
            comp_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FCE7F3')),
                ('BOX', (0, 0), (-1, -1), 0.5, color_gray),
            ]))
            elements.append(comp_table)
            elements.append(Spacer(1, 15))
        
        # ==== RÉSEAUX SOCIAUX ====
        social_networks = []
        social_fields = {
            'facebook': 'Facebook',
            'instagram': 'Instagram', 
            'twitter': 'Twitter',
            'youtube': 'YouTube',
            'tiktok': 'TikTok',
            'snapchat': 'Snapchat',
            'linkedin': 'LinkedIn',
            'telegram': 'Telegram',
            'imdb_url': 'IMDb',
            'threads': 'Threads'
        }
        
        for field, label in social_fields.items():
            encrypted_field = f'{field}_encrypted'
            if hasattr(cinema_talent, encrypted_field):
                encrypted_value = getattr(cinema_talent, encrypted_field)
                if encrypted_value:
                    try:
                        decrypted_value = decrypt_sensitive_data(encrypted_value)
                        if decrypted_value:
                            social_networks.append([label, decrypted_value])
                    except:
                        pass
        
        if social_networks:
            social_title = Table([['RÉSEAUX SOCIAUX']], colWidths=[6.5*inch])
            social_title.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#6366F1')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(social_title)
            
            social_table = Table(social_networks, colWidths=[1.5*inch, 5*inch])
            social_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E0E7FF')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, color_gray),
                ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
            ]))
            elements.append(social_table)
            elements.append(Spacer(1, 15))
        
        # ==== PRODUCTIONS PRÉCÉDENTES ====
        try:
            productions = json.loads(cinema_talent.previous_productions) if cinema_talent.previous_productions else []
        except:
            productions = []
        
        if productions:
            prod_title = Table([['PRODUCTIONS PRÉCÉDENTES']], colWidths=[6.5*inch])
            prod_title.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EF4444')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(prod_title)
            
            prod_data = []
            for production in productions:
                title = production.get('title', 'Sans titre')
                prod_type = production.get('type', '')
                year = production.get('year', '')
                prod_info = f"{title} ({prod_type}, {year})" if prod_type and year else title
                prod_data.append([prod_info])
            
            prod_table = Table(prod_data, colWidths=[6.5*inch])
            prod_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEE2E2')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, color_gray),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#FEE2E2')]),
            ]))
            elements.append(prod_table)
            elements.append(Spacer(1, 15))
        
        # ==== GALERIE PHOTO ====
        gallery_title = Table([['GALERIE PHOTO']], colWidths=[6.5*inch])
        gallery_title.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#8B5CF6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(gallery_title)
        
        # Collecter les miniatures de photos
        photo_thumbnails = []
        
        # Photo de profil
        if cinema_talent.profile_photo_filename:
            try:
                photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos', cinema_talent.profile_photo_filename)
                if os.path.exists(photo_path):
                    img = Image(photo_path, width=1.5*inch, height=1.5*inch)
                    label = Paragraph("<b>Photo de profil</b>", styles['Normal'])
                    photo_thumbnails.append([img, label])
            except:
                pass
        
        # Photo d'identité
        if cinema_talent.id_photo_filename:
            try:
                photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos', cinema_talent.id_photo_filename)
                if os.path.exists(photo_path):
                    img = Image(photo_path, width=1.5*inch, height=1.5*inch)
                    label = Paragraph("<b>Photo d'identité</b>", styles['Normal'])
                    photo_thumbnails.append([img, label])
            except:
                pass
        
        # Photos de la galerie
        try:
            gallery = json.loads(cinema_talent.gallery_photos) if cinema_talent.gallery_photos else []
            for idx, photo_filename in enumerate(gallery, 1):
                try:
                    photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos', photo_filename)
                    if os.path.exists(photo_path):
                        img = Image(photo_path, width=1.5*inch, height=1.5*inch)
                        label = Paragraph(f"<b>Photo {idx}</b>", styles['Normal'])
                        photo_thumbnails.append([img, label])
                except:
                    pass
        except:
            pass
        
        if photo_thumbnails:
            # Organiser les photos en grille (3 colonnes)
            photos_per_row = 3
            photo_rows = []
            for i in range(0, len(photo_thumbnails), photos_per_row):
                row_items = []
                for j in range(photos_per_row):
                    if i + j < len(photo_thumbnails):
                        photo_cell = photo_thumbnails[i + j]
                        # Créer une cellule avec l'image et le label
                        cell_content = Table([[photo_cell[0]], [photo_cell[1]]], colWidths=[1.5*inch])
                        cell_content.setStyle(TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ]))
                        row_items.append(cell_content)
                    else:
                        row_items.append('')
                photo_rows.append(row_items)
            
            photos_grid = Table(photo_rows, colWidths=[2.15*inch, 2.15*inch, 2.15*inch])
            photos_grid.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EDE9FE')),
                ('GRID', (0, 0), (-1, -1), 0.5, color_gray),
            ]))
            elements.append(photos_grid)
        else:
            no_photos_para = Paragraph("Aucune photo disponible", styles['Normal'])
            no_photos_table = Table([[no_photos_para]], colWidths=[6.5*inch])
            no_photos_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Oblique'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F3F4F6')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOX', (0, 0), (-1, -1), 0.5, color_gray),
            ]))
            elements.append(no_photos_table)
        elements.append(Spacer(1, 15))
        
        # ==== FOOTER ====
        elements.append(Spacer(1, 20))
        footer_line = Table([['']],  colWidths=[6.5*inch])
        footer_line.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, color_indigo),
        ]))
        elements.append(footer_line)
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=color_gray,
            alignment=TA_CENTER
        )
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", footer_style))
        elements.append(Paragraph("Plateforme taalentio.com CINEMA - Talents du Cinéma Africain", footer_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

def export_attendance_to_excel(project, attendances, start_date=None, end_date=None):
    """
    Exporter les présences d'un projet vers Excel
    
    Args:
        project: Objet Project
        attendances: Liste d'objets Attendance
        start_date: Date de début (optionnel)
        end_date: Date de fin (optionnel)
        
    Returns:
        Response Flask avec le fichier Excel
    """
    from flask import send_file
    from app.models.cinema_talent import CinemaTalent
    
    data = []
    
    for att in attendances:
        # Récupérer les infos du talent
        talent = CinemaTalent.query.filter_by(unique_code=att.cinema_talent_code).first()
        
        if talent:
            data.append({
                'Date': att.date.strftime('%d/%m/%Y'),
                'Code Cinéma': att.cinema_talent_code,
                'Prénom': talent.first_name,
                'Nom': talent.last_name,
                'Type': talent.talent_type or 'N/A',
                'Arrivée': att.check_in_time.strftime('%H:%M') if att.check_in_time else '-',
                'Départ': att.check_out_time.strftime('%H:%M') if att.check_out_time else 'En cours',
                'Durée': att.get_duration_formatted(),
                'Minutes': att.get_duration_minutes(),
                'Enregistré par': f"{att.recorder.first_name} {att.recorder.last_name}"
            })
    
    df = pd.DataFrame(data)
    
    # Créer le fichier Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Présences', index=False)
        
        worksheet = writer.sheets['Présences']
        
        # Ajuster la largeur des colonnes
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
    
    output.seek(0)
    
    # Nom du fichier
    period_str = ""
    if start_date and end_date:
        period_str = f"_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}"
    elif start_date:
        period_str = f"_{start_date.strftime('%Y%m%d')}"
    
    filename = f"presences_{project.name.replace(' ', '_')}{period_str}.xlsx"
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )
