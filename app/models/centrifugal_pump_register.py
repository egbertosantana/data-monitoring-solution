import logging
import random
import uuid
from app.adapters.database import db
from app.models.centrifugal_pump import CentrifugalPump  # Import CentrifugalPump to access existing pumps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        return (f"<CentrifugalPumpRegister(id={self.id}, energy_consumption={self.energy_consumption}, "
                f"flow_rate={self.flow_rate}, temperature={self.temperature}, vibration={self.vibration}, "
                f"pump_id={self.pump_id}, created_at={self.created_at}, moment_water_leak={self.moment_water_leak})>")

    def map(self):
        """Map the register to a dictionary format."""
        pump = CentrifugalPump.query.get(self.pump_id)
        if not pump:
            logger.warning(f"No pump found for pump_id={self.pump_id}.")
        return {
            "id": self.id,
            "energy_consumption": self.energy_consumption,
            "flow_rate": self.flow_rate,
            "temperature": self.temperature,
            "vibration": self.vibration,
            "moment_water_leak": self.moment_water_leak,
            "created_at": self.created_at.isoformat(),
            "pump": {
                "id": pump.id,
                "enabled": pump.enabled,
                "current_water_leak": pump.current_water_leak,
                "brand": pump.brand.name if pump.brand else None,
                "created_at": pump.created_at.isoformat() if pump.created_at else None,
                "updated_at": pump.updated_at.isoformat() if pump.updated_at else None,
            } if pump else None
        }
