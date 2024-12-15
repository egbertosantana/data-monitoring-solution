from flask import Blueprint
from app.controllers.centrifugal_pump_controller import CentrifugalPumpController

main = Blueprint("main", __name__)

# Instantiate the controller
centrifugal_pump_controller = CentrifugalPumpController()

@main.route("/centrifugal_pump/produce", methods=["POST"])
def produce():
    return centrifugal_pump_controller.produce()

@main.route("/centrifugal_pump/start", methods=["POST"])
def start():
    return centrifugal_pump_controller.start()

@main.route("/centrifugal_pump/stop", methods=["POST"])
def stop():
    return centrifugal_pump_controller.stop()
