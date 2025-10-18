from app import db

class Country(db.Model):
    __tablename__ = 'countries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(2), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<Country {self.code} - {self.name}>'

class City(db.Model):
    __tablename__ = 'cities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(3), nullable=False)
    
    def __repr__(self):
        return f'<City {self.code} - {self.name}>'
