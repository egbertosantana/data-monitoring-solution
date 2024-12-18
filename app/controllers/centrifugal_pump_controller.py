from flask import jsonify
from app.adapters.producer import ProducerService
from app.services.centrifugal_pump_register_service import CentrifugalPumpRegisterService

class CentrifugalPumpController:
    def __init__(self):
        self.producer_service = ProducerService(interval=10)

    def produce(self):
        """API endpoint to generate random pump register data."""
        registers = CentrifugalPumpRegisterService.produce_random_data()
        return jsonify({
            "message": f"{len(registers)} pump registers generated.",
            "data": [register.map() for register in registers]
        }), 201

    def start(self):
        self.producer_service.start()
        return jsonify({
            "result": "Producer starting to register actions from Centrifugal Pumps."
            }), 201

    def stop(self):
        message = self.producer_service.stop()
        if message:
            return jsonify({"result": message})
        return jsonify({
            "result": "Producer stopping to register actions from Centrifugal Pumps."
            }), 201