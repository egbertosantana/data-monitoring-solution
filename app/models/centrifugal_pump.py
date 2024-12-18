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
        return (
            f"<CentrifugalPump(id={self.id}, max_temp={self.maximum_temperature}, "
            f"min_head={self.minimum_head}, max_head={self.maximum_head}, "
            f"max_flow={self.maximum_flow}, motor_voltage={self.motor_voltage}, "
            f"discharge_dia={self.discharge_diameter}, suction_dia={self.suction_diameter}, "
            f"impeller={self.impeller}, material={self.impeller_material}, "
            f"frequency={self.motor_frequency}, leak={self.current_water_leak}, "
            f"enabled={self.enabled})>"
        )

    @staticmethod
    def populate():
        brands = {
            "Ferrari": ["Closed", "Open"],
            "Grundfos": ["Semi-open", "Closed"],
            "KSB": ["Open", "Closed", "Semi-open"],
            "Schneider": ["Closed"],
            "Thebe": ["Semi-open"],
            "Ebara": ["Open", "Closed"],
            "Heliotek": ["Semi-open", "Open"]
        }

        pumps = []
        for brand_name, impeller_types in brands.items():
            brand_entity = Brand.query.filter_by(name=brand_name).first()
            if not brand_entity:
                print(f"Warning: Brand {brand_name} not found in the database.")
                continue

            if not CentrifugalPump.query.filter_by(brand_id=brand_entity.id).first():
                pump = CentrifugalPump(
                    maximum_temperature=round(random.uniform(50.0, 150.0), 2),
                    minimum_head=round(random.uniform(5.0, 20.0), 2),
                    maximum_head=round(random.uniform(30.0, 60.0), 2),
                    maximum_flow=round(random.uniform(1000.0, 5000.0), 2),
                    motor_voltage=random.choice([220, 380, 415]),
                    discharge_diameter=round(random.uniform(50.0, 200.0), 2),
                    suction_diameter=round(random.uniform(50.0, 200.0), 2),
                    impeller=random.choice(impeller_types),
                    impeller_material=random.choice(["Stainless Steel", "Bronze", "Cast Iron", "Plastic"]),
                    motor_frequency=round(random.uniform(50.0, 60.0), 2),
                    brand=brand_entity
                )
                pumps.append(pump)

        db.session.add_all(pumps)
        db.session.commit()
        print(f"{len(pumps)} random centrifugal pumps generated and added to the database!")

    @staticmethod
    def set_enabled_status(enabled: bool):
        pumps = CentrifugalPump.query.all()
        for pump in pumps:
            pump.enabled = enabled
        db.session.commit()

    @staticmethod
    def activate():
        CentrifugalPump.set_enabled_status(True)

    @staticmethod
    def deactivate():
        CentrifugalPump.set_enabled_status(False)

