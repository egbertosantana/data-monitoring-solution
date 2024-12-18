from flask import jsonify
from app.adapters.producer import ProducerAdapter
from app.services.centrifugal_pump_register_service import CentrifugalPumpRegisterService
import logging

logger = logging.getLogger(__name__)

class CentrifugalPumpController:
    def __init__(self):
        self.producer_service = ProducerAdapter(interval=10)

    def produce(self):
        """API endpoint to generate random pump register data."""
        try:
            registers = CentrifugalPumpRegisterService.produce_random_data()
            return jsonify({
                "message": f"{len(registers)} pump registers generated.",
                "data": [register.map() for register in registers]
            }), 201
        except Exception as e:
            logger.error(f"Error in producing pump registers: {e}")
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

    def start(self):
        """Start the producer service."""
        try:
            self.producer_service.start()
            return jsonify({
                "result": "Producer starting to register actions from Centrifugal Pumps."
            }), 201
        except Exception as e:
            logger.error(f"Error starting the producer service: {e}")
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

    def stop(self):
        """Stop the producer service."""
        try:
            message = self.producer_service.stop()
            if message:
                return jsonify({"result": message})
            return jsonify({
                "result": "Producer stopping to register actions from Centrifugal Pumps."
            }), 201
        except Exception as e:
            logger.error(f"Error stopping the producer service: {e}")
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
