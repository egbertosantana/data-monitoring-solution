from app.adapters.database import db

class Brand(db.Model):
    __tablename__ = 'brand'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False, comment="Brand name")
    pumps = db.relationship('CentrifugalPump', back_populates='brand', lazy='dynamic')  # Relation to CentrifugalPump
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<Brand(id={self.id}, name='{self.name}')>"
    
    @staticmethod
    def populate():
        brands = ["Ferrari", "Grundfos", "KSB", "Schneider", "Thebe", "Ebara", "Heliotek"]
        for brand_name in brands:
            brand = Brand.query.filter_by(name=brand_name).first()
            
            if not brand:
                brand = Brand(name=brand_name)
                db.session.add(brand)
        db.session.commit()
