from app.adapters.database import db
import random
from app.models.centrifugal_pump import CentrifugalPump  # Import CentrifugalPump to access existing pumps
import uuid

class CentrifugalPumpRegister(db.Model):
    __tablename__ = 'centrifugal_pump_register'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), comment="UUID as primary key")
    energy_consumption = db.Column(db.Float, nullable=False, comment="Energy consumption in kWh")
    flow_rate = db.Column(db.Float, nullable=False, comment="Flow rate in liters/hour")
    temperature = db.Column(db.Float, nullable=False, comment="Temperature in °C")
    vibration = db.Column(db.Float, nullable=False, comment="Vibration in Hz")
    pump_id = db.Column(db.Integer, db.ForeignKey('centrifugal_pump.id'), nullable=False, comment="Associated pump ID")
    moment_water_leak = db.Column(db.Float, nullable=False, comment="Water leak volume lost in this moment (liters)")
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False, comment="Timestamp when data was recorded")

    def __repr__(self):
            return (f"<PumpData(id={self.id}, energy_consumption={self.energy_consumption}, "
                    f"flow_rate={self.flow_rate}, temperature={self.temperature}, vibration={self.vibration}, "
                    f"pump_id={self.pump_id}, created_at={self.created_at}, moment_water_leak={self.moment_water_leak})>")

    @classmethod
    def produce(cls):
        # Query existing pumps in the database
        pumps = CentrifugalPump.query.all()
        
        if not pumps:
            print("No pumps found in the database. Please create pumps first.")
            return


        registers = []
        # Iterate through all pumps and generate a register for each pump
        for pump in pumps:
            # Generate random data and insert into the register

            if pump.enabled:
                current_water_leak = pump.current_water_leak
                new_water_leak = round(random.uniform(0.0, 0.01), 4)
                updated_water_leak = current_water_leak + new_water_leak
                pump.current_water_leak = updated_water_leak
                pump.updated_at = db.func.now()
                
                random_data = CentrifugalPumpRegister(
                    energy_consumption=round(random.uniform(10.0, 100.0), 2),  # Random float between 10 and 100
                    flow_rate=round(random.uniform(5.0, 50.0), 2),  # Random float between 5 and 50
                    temperature=round(random.uniform(20.0, 80.0), 2),  # Random float between 20 and 80
                    vibration=round(random.uniform(0.1, 5.0), 2),  # Random float between 0.1 and 5.0
                    moment_water_leak=new_water_leak,
                    pump_id=pump.id  # Associate the random data with the current pump
                )
                registers.append(random_data)

        db.session.add_all(registers)
        db.session.commit()
        print(f"Random PumpData entries inserted for {len(pumps)} pumps!")

        return registers

    def map(self):
        return {
            "id": self.id,
            "energy_consumption": self.energy_consumption,
            "flow_rate": self.flow_rate,
            "temperature": self.temperature,
            "vibration": self.vibration,
            "moment_water_leak": self.moment_water_leak,
            "created_at": self.created_at.isoformat(),
            "pump": CentrifugalPump.map(CentrifugalPump.query.filter_by(id=self.pump_id).first()) # Format datetime to ISO string
        }
