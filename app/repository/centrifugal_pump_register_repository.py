from app.adapters.database import db
from app.models.centrifugal_pump import CentrifugalPump
from app.models.centrifugal_pump_register import CentrifugalPumpRegister


class CentrifugalPumpRegisterRepository:
    @staticmethod
    def get_all_enabled_pumps():
        """Retrieve all enabled pumps from the database."""
        return CentrifugalPump.query.filter_by(enabled=True).all()

    @staticmethod
    def add_registers(registers):
        """Add a list of registers to the database."""
        db.session.add_all(registers)
        db.session.commit()

    @staticmethod
    def update_pump(pump):
        """Update a single pump's details."""
        db.session.add(pump)
        db.session.commit()
