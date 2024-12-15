from app.repository.centrifugal_pump_repository import CentrifugalPumpRepository

class CentrifugalPumpService:
    @staticmethod
    def map_pump_data(pump):
        return {
            "id": pump.id,
            "maximum_temperature": pump.maximum_temperature,
            "minimum_head": pump.minimum_head,
            "maximum_head": pump.maximum_head,
            "maximum_flow": pump.maximum_flow,
            "motor_voltage": pump.motor_voltage,
            "discharge_diameter": pump.discharge_diameter,
            "suction_diameter": pump.suction_diameter,
            "impeller": pump.impeller,
            "impeller_material": pump.impeller_material,
            "motor_frequency": pump.motor_frequency,
            "current_water_leak": pump.current_water_leak,
            "enabled": pump.enabled,
            "brand": pump.brand.name if pump.brand else None,  # Accessing brand name
            "created_at": pump.created_at.isoformat() if pump.created_at else None,
            "updated_at": pump.updated_at.isoformat() if pump.updated_at else None
        }

    @staticmethod
    def activate_pumps():
        pumps = CentrifugalPumpRepository.get_all()
        for pump in pumps:
            pump.enabled = True
        CentrifugalPumpRepository.add_all(pumps)

    @staticmethod
    def deactivate_pumps():
        pumps = CentrifugalPumpRepository.get_all()
        for pump in pumps:
            pump.enabled = False
        CentrifugalPumpRepository.add_all(pumps)

    @staticmethod
    def populate_pumps():
        CentrifugalPumpRepository.populate_pumps()
