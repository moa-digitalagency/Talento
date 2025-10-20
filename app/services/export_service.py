"""
Service d'export des données des talents
Supporte Excel (XLSX), CSV, et PDF
"""
import os
import io
from datetime import datetime
from flask import current_app
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

class ExportService:
    """Service d'export des données"""
    
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
                'Pays': user.country.name if user.country else 'N/A',
                'Ville au Maroc': user.city.name if user.city else 'N/A',
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
                'Pays': user.country.name if user.country else 'N/A',
                'Ville au Maroc': user.city.name if user.city else 'N/A',
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
        
        data = [['Code', 'Nom Complet', 'Talents', 'Ville au Maroc', 'Pays Origine', 'Téléphone', 'WhatsApp']]
        
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
                user.city.name if user.city else 'N/A',
                user.country.name if user.country else 'N/A',
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
        
        elements.append(Paragraph("🌍 TALENTO - FICHE DE TALENT", header_style))
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
        
        # QR Code - devrait toujours exister car généré avec le code unique
        qr_element = None
        if user.qr_code_filename:
            try:
                qr_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'qrcodes', user.qr_code_filename)
                if os.path.exists(qr_path):
                    qr_element = Image(qr_path, width=1.5*inch, height=1.5*inch)
            except:
                pass
        
        # Placeholder simple pour QR code si vraiment absent
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
        identity_title = Table([['👤  IDENTITÉ']], colWidths=[6.5*inch])
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
        
        info_data = [
            ['Email', user.email or 'Information non disponible'],
            ['Téléphone', user.phone or 'Information non disponible'],
            ['WhatsApp', user.whatsapp or 'Information non disponible'],
            ['Adresse', user.address or 'Information non disponible'],
            ['Date de naissance', user.date_of_birth.strftime('%d/%m/%Y') if user.date_of_birth else 'Information non disponible'],
            ['Genre', {'M': 'Masculin', 'F': 'Féminin', 'N': 'Non précisé'}.get(user.gender, 'Information non disponible')],
            ['Pays d\'origine', user.country.name if user.country else 'Information non disponible'],
            ['Ville au Maroc', user.city.name if user.city else 'Information non disponible'],
            ['Langues', user.languages or 'Information non disponible'],
            ['Années d\'expérience', str(user.years_experience) + ' ans' if user.years_experience else 'Information non disponible'],
            ['Éducation', user.education or 'Information non disponible'],
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
            talents_title = Table([['🎯  TALENTS & COMPÉTENCES']], colWidths=[6.5*inch])
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
                talents_by_category[category].append(f"{ut.talent.emoji} {ut.talent.name}")
            
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
        prof_title = Table([['💼  PROFIL PROFESSIONNEL']], colWidths=[6.5*inch])
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
            ['CV disponible', '✓ Oui' if user.cv_filename else '✗ Non'],
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
            bio_title = Table([['📝  BIOGRAPHIE']], colWidths=[6.5*inch])
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
            social_title = Table([['🌐  RÉSEAUX SOCIAUX']], colWidths=[6.5*inch])
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
        elements.append(Paragraph("🌍 Plateforme Talento - Centralisation des Talents Africains", footer_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
