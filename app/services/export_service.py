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
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

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
    def export_list_to_pdf(users, filename='talents_list.pdf'):
        """
        Exporter la liste des talents vers PDF (format tableau)
        
        Args:
            users: Liste d'objets User
            filename: Nom du fichier de sortie
            
        Returns:
            bytes: Données du fichier PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4F46E5'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph("Liste des Talents Talento", title_style))
        elements.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        data = [['Code', 'Nom Complet', 'Talents', 'Pays', 'Score']]
        
        for user in users[:50]:
            talents_names = [ut.talent.name for ut in user.talents[:3]] if user.talents else []
            talents_str = ', '.join(talents_names)
            if len(user.talents) > 3:
                talents_str += f' +{len(user.talents)-3}'
            
            data.append([
                user.unique_code[:10],
                f"{user.first_name} {user.last_name}"[:25],
                talents_str[:30],
                user.country.code if user.country else 'N/A',
                str(user.profile_score or 0)
            ])
        
        table = Table(data, colWidths=[1.5*inch, 2*inch, 2.5*inch, 0.8*inch, 0.6*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(table)
        
        if len(users) > 50:
            elements.append(Spacer(1, 20))
            elements.append(Paragraph(f"Note: Affichage limité aux 50 premiers talents (Total: {len(users)})", styles['Italic']))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    @staticmethod
    def export_talent_card_pdf(user):
        """
        Générer une fiche talent individuelle en PDF
        
        Args:
            user: Objet User
            
        Returns:
            bytes: Données du fichier PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#4F46E5'),
            spaceAfter=10,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        section_style = ParagraphStyle(
            'Section',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#4F46E5'),
            spaceAfter=10,
            spaceBefore=15
        )
        
        elements.append(Paragraph("FICHE TALENT", title_style))
        elements.append(Paragraph(f"Code: {user.formatted_code}", subtitle_style))
        elements.append(Spacer(1, 20))
        
        if user.photo_filename:
            try:
                photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos', user.photo_filename)
                if os.path.exists(photo_path):
                    img = Image(photo_path, width=2*inch, height=2*inch)
                    img.hAlign = 'CENTER'
                    elements.append(img)
                    elements.append(Spacer(1, 20))
            except:
                pass
        
        elements.append(Paragraph("IDENTITÉ", section_style))
        info_data = [
            ['Nom complet:', f"{user.first_name} {user.last_name}"],
            ['Email:', user.email],
            ['Téléphone:', user.phone or 'Non renseigné'],
            ['WhatsApp:', user.whatsapp or 'Non renseigné'],
        ]
        
        if user.date_of_birth:
            info_data.append(['Date de naissance:', user.date_of_birth.strftime('%d/%m/%Y')])
        
        info_data.extend([
            ['Genre:', {'M': 'Masculin', 'F': 'Féminin', 'N': 'Non précisé'}.get(user.gender, 'Non précisé')],
            ['Pays d\'origine:', user.country.name if user.country else 'Non renseigné'],
        ])
        
        if user.city:
            info_data.append(['Ville au Maroc:', user.city.name])
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 15))
        
        if user.talents:
            elements.append(Paragraph("TALENTS & COMPÉTENCES", section_style))
            talents_by_category = {}
            for ut in user.talents:
                category = ut.talent.category
                if category not in talents_by_category:
                    talents_by_category[category] = []
                talents_by_category[category].append(f"{ut.talent.emoji} {ut.talent.name}")
            
            for category, talents in talents_by_category.items():
                elements.append(Paragraph(f"<b>{category}:</b> {', '.join(talents)}", styles['Normal']))
            elements.append(Spacer(1, 15))
        
        elements.append(Paragraph("PROFIL PROFESSIONNEL", section_style))
        prof_data = [
            ['Disponibilité:', user.availability or 'Non renseigné'],
            ['Mode de travail:', user.work_mode or 'Non renseigné'],
            ['Fourchette tarifaire:', user.rate_range or 'Non renseigné'],
            ['Score de profil:', f"{user.profile_score or 0}/100"],
            ['CV:', 'Oui ✓' if user.cv_filename else 'Non ✗'],
            ['Portfolio:', 'Oui ✓' if user.portfolio_url else 'Non ✗'],
        ]
        
        prof_table = Table(prof_data, colWidths=[2*inch, 4*inch])
        prof_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ]))
        elements.append(prof_table)
        elements.append(Spacer(1, 15))
        
        if user.bio:
            elements.append(Paragraph("BIOGRAPHIE", section_style))
            elements.append(Paragraph(user.bio, styles['Normal']))
            elements.append(Spacer(1, 15))
        
        social_links = []
        for platform in ['linkedin', 'instagram', 'twitter', 'facebook', 'github', 'behance']:
            value = getattr(user, platform, None)
            if value:
                social_links.append([platform.capitalize(), value])
        
        if social_links:
            elements.append(Paragraph("RÉSEAUX SOCIAUX", section_style))
            social_table = Table(social_links, colWidths=[1.5*inch, 4.5*inch])
            social_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            elements.append(social_table)
        
        elements.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", footer_style))
        elements.append(Paragraph("Plateforme Talento - Centralisation des Talents", footer_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
