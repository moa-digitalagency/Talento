import os
from app import create_app, db
from app.models import User, Talent, UserTalent, Country, City

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Talent': Talent,
        'UserTalent': UserTalent,
        'Country': Country,
        'City': City
    }

@app.template_filter('format_code')
def format_code_filter(code):
    """Format code with dashes for display"""
    if code and len(code) == 10:
        return f"{code[:2]}-{code[2:5]}-{code[5:9]}-{code[9]}"
    return code

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
