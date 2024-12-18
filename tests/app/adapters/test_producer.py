import pytest
from unittest import mock
import time
from threading import Thread
from app.services.centrifugal_pump_service import CentrifugalPumpService
from app.services.centrifugal_pump_register_service import CentrifugalPumpRegisterService
from app.adapters.producer import ProducerAdapter

# Mocking the CentrifugalPumpService and CentrifugalPumpRegisterService
@pytest.fixture
def mock_centrifugal_pump_service():
    return mock.Mock(spec=CentrifugalPumpService)

@pytest.fixture
def mock_centrifugal_pump_register_service():
    return mock.Mock(spec=CentrifugalPumpRegisterService)

@pytest.fixture
def producer_adapter(mock_centrifugal_pump_service, mock_centrifugal_pump_register_service):
    return ProducerAdapter(interval=2)

class TestProducerAdapter:
    @mock.patch('app.adapters.producer.CentrifugalPumpService', new_callable=mock.Mock)
    @mock.patch('app.adapters.producer.CentrifugalPumpRegisterService', new_callable=mock.Mock)
    def test_start(self, MockCentrifugalPumpService, MockCentrifugalPumpRegisterService, producer_adapter):
        """Test start method for the ProducerAdapter."""
        # Arrange
        mock_centrifugal_pump_service = MockCentrifugalPumpService.return_value
        mock_centrifugal_pump_register_service = MockCentrifugalPumpRegisterService.return_value

        # Act
        producer_adapter.start()

        # Assert
        mock_centrifugal_pump_service.activate_pumps.assert_called_once()
        mock_centrifugal_pump_register_service.produce_random_data.assert_called()
        assert producer_adapter.running is True
        assert isinstance(producer_adapter.thread, Thread)

    @mock.patch('app.adapters.producer.CentrifugalPumpService', new_callable=mock.Mock)
    @mock.patch('app.adapters.producer.CentrifugalPumpRegisterService', new_callable=mock.Mock)
    def test_stop(self, MockCentrifugalPumpService, MockCentrifugalPumpRegisterService, producer_adapter):
        """Test stop method for the ProducerAdapter."""
        # Arrange
        mock_centrifugal_pump_service = MockCentrifugalPumpService.return_value
        mock_centrifugal_pump_register_service = MockCentrifugalPumpRegisterService.return_value

        # Start the producer
        producer_adapter.start()

        # Act
        producer_adapter.stop()

        # Assert
        mock_centrifugal_pump_service.deactivate_pumps.assert_called_once()
        mock_centrifugal_pump_register_service.produce_random_data.assert_called()
        assert producer_adapter.running is False
        assert producer_adapter.thread.is_alive() is False

    @mock.patch('app.adapters.producer.CentrifugalPumpService', new_callable=mock.Mock)
    @mock.patch('app.adapters.producer.CentrifugalPumpRegisterService', new_callable=mock.Mock)
    def test_start_already_running(self, MockCentrifugalPumpService, MockCentrifugalPumpRegisterService, producer_adapter):
        """Test start method when the service is already running."""
        # Arrange
        mock_centrifugal_pump_service = MockCentrifugalPumpService.return_value
        mock_centrifugal_pump_register_service = MockCentrifugalPumpRegisterService.return_value

        # Act
        producer_adapter.start()
        # Try to start again while it is already running
        producer_adapter.start()

        # Assert
        mock_centrifugal_pump_service.activate_pumps.assert_called_once()  # Should be called once
        mock_centrifugal_pump_register_service.produce_random_data.assert_called()  # Should be called at least once
        assert producer_adapter.running is True  # The service should still be running
        assert isinstance(producer_adapter.thread, Thread)

    @mock.patch('app.adapters.producer.CentrifugalPumpService', new_callable=mock.Mock)
    @mock.patch('app.adapters.producer.CentrifugalPumpRegisterService', new_callable=mock.Mock)
    def test_stop_not_started(self, MockCentrifugalPumpService, MockCentrifugalPumpRegisterService, producer_adapter):
        """Test stop method when the producer service was not started."""
        # Arrange
        mock_centrifugal_pump_service = MockCentrifugalPumpService.return_value
        mock_centrifugal_pump_register_service = MockCentrifugalPumpRegisterService.return_value

        # Act
        producer_adapter.stop()

        # Assert
        mock_centrifugal_pump_service.deactivate_pumps.assert_not_called()
        mock_centrifugal_pump_register_service.produce_random_data.assert_not_called()
        assert producer_adapter.running is False
        assert producer_adapter.thread is None

    @mock.patch('app.adapters.producer.time.sleep', return_value=None)
    @mock.patch('app.adapters.producer.CentrifugalPumpService', new_callable=mock.Mock)
    @mock.patch('app.adapters.producer.CentrifugalPumpRegisterService', new_callable=mock.Mock)
    def test_threading_behavior(self, MockCentrifugalPumpService, MockCentrifugalPumpRegisterService, mock_sleep, producer_adapter):
        """Test the threading behavior of the ProducerAdapter."""
        # Arrange
        mock_centrifugal_pump_service = MockCentrifugalPumpService.return_value
        mock_centrifugal_pump_register_service = MockCentrifugalPumpRegisterService.return_value

        # Act
        producer_adapter.start()

        # Simulate some time for the thread to run
        time.sleep(3)

        # Assert
        mock_centrifugal_pump_register_service.produce_random_data.assert_called()
        assert producer_adapter.running is True
        assert isinstance(producer_adapter.thread, Thread)
        assert producer_adapter.thread.is_alive()

        # Stop the producer
        producer_adapter.stop()

        # Assert the thread is no longer running
        assert not producer_adapter.thread.is_alive()
