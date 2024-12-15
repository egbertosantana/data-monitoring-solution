from flask import jsonify
from app.adapters.producer import ProducerService
from app.models import CentrifugalPumpRegister

class CentrifugalPumpController:
    def __init__(self):
        self.producer_service = ProducerService(interval=10)

    def produce(self):
        registers = CentrifugalPumpRegister.produce()
        return jsonify([pump.map() for pump in registers])

    def start(self):
        self.producer_service.start()
        return jsonify({"result": "Producer starting to register actions from Centrifugal Pumps."})

    def stop(self):
        message = self.producer_service.stop()
        if message:
            return jsonify({"result": message})
        return jsonify({"result": "Producer stopping to register actions from Centrifugal Pumps."})
