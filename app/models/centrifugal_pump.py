from app.adapters.database import db
from app.models.brand import Brand
import random

class CentrifugalPump(db.Model):
    __tablename__ = 'centrifugal_pump'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maximum_temperature = db.Column(db.Float, nullable=False, comment="Maximum operating temperature (°C)")
    minimum_head = db.Column(db.Float, nullable=False, comment="Minimum head (m.c.a)")
    maximum_head = db.Column(db.Float, nullable=False, comment="Maximum head (m.c.a)")
    maximum_flow = db.Column(db.Float, nullable=False, comment="Maximum flow (liters/hour)")
    motor_voltage = db.Column(db.Integer, nullable=False, comment="Motor voltage (V)")
    discharge_diameter = db.Column(db.Float, nullable=False, comment="Discharge diameter (mm)")
    suction_diameter = db.Column(db.Float, nullable=False, comment="Suction diameter (mm)")
    impeller = db.Column(db.String(255), nullable=False, comment="Impeller type")
    impeller_material = db.Column(db.String(255), nullable=False, comment="Material of the impeller")
    motor_frequency = db.Column(db.Float, nullable=False, comment="Motor frequency (Hz)")
    current_water_leak = db.Column(db.Float, nullable=False, default=0.0, comment="Current water leak volume (liters)")
    enabled = db.Column(db.Boolean, default=False, nullable=False, comment="Indicates whether the pump is enabled or disabled")
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False, comment="Brand of the pump")
    brand = db.relationship('Brand', back_populates='pumps')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return (f"<CentrifugalPump(id={self.id}, maximum_temperature={self.maximum_temperature}, "
                f"minimum_head={self.minimum_head}, maximum_head={self.maximum_head}, "
                f"maximum_flow={self.maximum_flow}, motor_voltage={self.motor_voltage}, "
                f"discharge_diameter={self.discharge_diameter}, suction_diameter={self.suction_diameter}, "
                f"impeller='{self.impeller}', impeller_material='{self.impeller_material}', "
                f"motor_frequency={self.motor_frequency}, current_water_leak={self.current_water_leak}, "
                f"enabled={self.enabled})>")

    
    @staticmethod
    def populate():
        brands = ["Ferrari", "Grundfos", "KSB", "Schneider", "Thebe", "Ebara", "Heliotek"]
        impeller_map = {
            "Ferrari": ["Closed", "Open"],
            "Grundfos": ["Semi-open", "Closed"],
            "KSB": ["Open", "Closed", "Semi-open"],
            "Schneider": ["Closed"],
            "Thebe": ["Semi-open"],
            "Ebara": ["Open", "Closed"],
            "Heliotek": ["Semi-open", "Open"]
        }

        pumps = []
        for brand in brands:
            brand_entity = Brand.query.filter_by(name=brand).first()
            impeller_type = random.choice(impeller_map[brand])

            pump = CentrifugalPump(
                maximum_temperature=round(random.uniform(50.0, 150.0), 2),
                minimum_head=round(random.uniform(5.0, 20.0), 2),
                maximum_head=round(random.uniform(30.0, 60.0), 2),
                maximum_flow=round(random.uniform(1000.0, 5000.0), 2),
                motor_voltage=random.choice([220, 380, 415]),
                discharge_diameter=round(random.uniform(50.0, 200.0), 2),
                suction_diameter=round(random.uniform(50.0, 200.0), 2),
                impeller=impeller_type,
                impeller_material=random.choice(["Stainless Steel", "Bronze", "Cast Iron", "Plastic"]),
                motor_frequency=round(random.uniform(50.0, 60.0), 2),
                brand=brand_entity
            )
            existing_pump = CentrifugalPump.query.filter_by(brand_id=brand_entity.id).first()
            
            if not existing_pump:
                pumps.append(pump)

        db.session.add_all(pumps)
        db.session.commit()
        print(f"{len(pumps)} Random Centrifugal Pumps generated and added to the database!")

    def map(self):
        return {
            "id": self.id,
            "maximum_temperature": self.maximum_temperature,
            "minimum_head": self.minimum_head,
            "maximum_head": self.maximum_head,
            "maximum_flow": self.maximum_flow,
            "motor_voltage": self.motor_voltage,
            "discharge_diameter": self.discharge_diameter,
            "suction_diameter": self.suction_diameter,
            "impeller": self.impeller,
            "impeller_material": self.impeller_material,
            "motor_frequency": self.motor_frequency,
            "current_water_leak": self.current_water_leak,
            "enabled": self.enabled,
            "brand": self.brand.name if self.brand else None,  # Accessing brand name
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def activate():
        pumps = CentrifugalPump.query.all()

        for pump in pumps:
            pump.enabled = True
        
        db.session.commit()

    @staticmethod
    def deactivate():
        pumps = CentrifugalPump.query.all()

        for pump in pumps:
            pump.enabled = False
        
        db.session.commit()