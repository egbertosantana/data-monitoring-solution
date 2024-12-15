from app.adapters.database import db
from app.models.centrifugal_pump import CentrifugalPump
from app.models.brand import Brand

class CentrifugalPumpRepository:
    @staticmethod
    def get_all():
        return CentrifugalPump.query.all()

    @staticmethod
    def get_by_brand_id(brand_id):
        return CentrifugalPump.query.filter_by(brand_id=brand_id).first()

    @staticmethod
    def add_all(pumps):
        db.session.add_all(pumps)
        db.session.commit()

    @staticmethod
    def populate_pumps():
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
            existing_pump = CentrifugalPumpRepository.get_by_brand_id(brand_entity.id)
            
            if not existing_pump:
                pumps.append(pump)

        CentrifugalPumpRepository.add_all(pumps)
        print(f"{len(pumps)} Random Centrifugal Pumps generated and added to the database!")
