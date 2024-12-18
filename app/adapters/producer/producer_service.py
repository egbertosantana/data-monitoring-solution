import threading
import time
import logging
from threading import Lock
from app.services.centrifugal_pump_service import CentrifugalPumpService
from app.services.centrifugal_pump_register_service import CentrifugalPumpRegisterService

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

class ProducerService:
    def __init__(self, interval: int = 10):
        self.interval = interval
        self.thread = None
        self.running = False
        self._lock = Lock()

        # Dependency Injection of service classes
        self.centrifugal_pump_service = CentrifugalPumpService()
        self.centrifugal_pump_register_service = CentrifugalPumpRegisterService()

    def start(self):
        with self._lock:
            if not self.running:
                self.running = True
                self.thread = threading.Thread(target=self._produce_data)
                self.thread.start()
                self._activate_centrifugal_pump()
                logging.info("Producer service started.")
            else:
                logging.warning("Producer service is already running.")

    def stop(self):
        with self._lock:
            if self.running:
                self.running = False
                self.thread.join()
                logging.info("Producer service stopped.")
                self._deactivate_pumps()
            else:
                logging.warning("Producer service was not started.")

    def _produce_data(self):
        from app import create_app
        app = create_app()
        with app.app_context():
            while self.running:
                self._generate_pump_data()
                time.sleep(self.interval)

    def _generate_pump_data(self):
        self.centrifugal_pump_register_service.produce_random_data()

    def _activate_centrifugal_pump(self):
        self.centrifugal_pump_service.activate_pumps()

    def _deactivate_pumps(self):
        self.centrifugal_pump_service.deactivate_pumps()
