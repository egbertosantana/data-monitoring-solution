# services/centrifugal_pump_register_service.py

import logging
import random
from app.repository.centrifugal_pump_register_repository import CentrifugalPumpRegisterRepository
from app.models.centrifugal_pump_register import CentrifugalPumpRegister
from datetime import datetime

logger = logging.getLogger(__name__)


class CentrifugalPumpRegisterService:

    @staticmethod
    def produce_random_data():
        """Generate random data entries for all enabled pumps and update their state."""
        pumps = CentrifugalPumpRegisterRepository.get_all_enabled_pumps()

        if not pumps:
            logger.warning("No enabled pumps found in the database.")
            return []

        registers = []
        for pump in pumps:
            # Generate random data
            new_water_leak = round(random.uniform(0.0, 0.01), 4)
            pump.current_water_leak += new_water_leak
            pump.updated_at = datetime.now()

            random_register = CentrifugalPumpRegister(
                energy_consumption=round(random.uniform(10.0, 100.0), 2),
                flow_rate=round(random.uniform(5.0, 50.0), 2),
                temperature=round(random.uniform(20.0, 80.0), 2),
                vibration=round(random.uniform(0.1, 5.0), 2),
                moment_water_leak=new_water_leak,
                pump_id=pump.id
            )
            registers.append(random_register)

            # Update pump in the database
            CentrifugalPumpRegisterRepository.update_pump(pump)

        # Save registers to the database
        CentrifugalPumpRegisterRepository.add_registers(registers)
        logger.info(f"Generated and inserted {len(registers)} entries for enabled pumps.")
        return registers
