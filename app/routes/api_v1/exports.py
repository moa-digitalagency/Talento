"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask import request, jsonify, current_app, send_file
from flask_login import login_required, current_user
from app.routes.api_v1 import bp
from app.models.user import User
from app.services.export_service import ExportService
from functools import wraps
import io
from datetime import datetime

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({
                'success': False,
                'error': 'Admin access required'
            }), 403
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/export/users/excel', methods=['GET'])
@login_required
@admin_required
def export_users_excel():
    """
    Export all users to Excel
    ---
    GET /api/v1/export/users/excel
    
    Response: Excel file download
    """
    try:
        users = User.query.filter(User.is_admin == False).all()
        excel_bytes = ExportService.export_to_excel(users)
        
        buffer = io.BytesIO(excel_bytes)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'talento_users_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
        
    except Exception as e:
        current_app.logger.error(f'Export users Excel API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@bp.route('/export/users/csv', methods=['GET'])
@login_required
@admin_required
def export_users_csv():
    """
    Export all users to CSV
    ---
    GET /api/v1/export/users/csv
    
    Response: CSV file download
    """
    try:
        users = User.query.filter(User.is_admin == False).all()
        csv_bytes = ExportService.export_to_csv(users)
        
        buffer = io.BytesIO(csv_bytes)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'talento_users_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        current_app.logger.error(f'Export users CSV API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@bp.route('/export/users/pdf', methods=['POST'])
@login_required
@admin_required
def export_users_pdf():
    """
    Export selected users to PDF
    ---
    POST /api/v1/export/users/pdf
    
    Request Body:
    {
        "user_ids": [1, 2, 3, 4]
    }
    
    Response: PDF file download
    """
    try:
        data = request.get_json()
        user_ids = data.get('user_ids', [])
        
        if not user_ids:
            return jsonify({
                'success': False,
                'error': 'No user IDs provided'
            }), 400
        
        users = User.query.filter(User.id.in_(user_ids)).all()
        
        if not users:
            return jsonify({
                'success': False,
                'error': 'No users found'
            }), 404
        
        pdf_bytes = ExportService.export_to_pdf(users)
        
        buffer = io.BytesIO(pdf_bytes)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'talento_users_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
        
    except Exception as e:
        current_app.logger.error(f'Export users PDF API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
