from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    """Inventory item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    
    def __repr__(self):
        return f'<Item {self.name}>'
