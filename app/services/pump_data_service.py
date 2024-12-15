from app.models.centrifugal_pump_register import CentrifugalPumpRegister
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

class PumpDataService:
    
    @staticmethod
    def generate_pump_data():
        try:
            CentrifugalPumpRegister.produce()
            logging.info("New pump data generated and inserted.")
        except Exception as e:
            logging.error(f"Error occurred while generating pump data: {str(e)}")
