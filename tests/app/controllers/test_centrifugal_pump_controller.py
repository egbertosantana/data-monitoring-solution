import pytest
from unittest import mock
from flask import Flask, jsonify
from app.controllers.centrifugal_pump_controller import CentrifugalPumpController
from app.services.centrifugal_pump_register_service import CentrifugalPumpRegisterService
from app.adapters.producer import ProducerAdapter

@pytest.fixture
def mock_producer_adapter():
    return mock.Mock(spec=ProducerAdapter)

@pytest.fixture
def mock_centrifugal_pump_register_service():
    return mock.Mock(spec=CentrifugalPumpRegisterService)

@pytest.fixture
def centrifugal_pump_controller(mock_producer_adapter, mock_centrifugal_pump_register_service):
    """Fixture to instantiate CentrifugalPumpController with mocked dependencies."""
    controller = CentrifugalPumpController()
    controller.producer_service = mock_producer_adapter
    return controller

class TestCentrifugalPumpController:

    @mock.patch('app.controllers.centrifugal_pump_controller.CentrifugalPumpRegisterService.produce_random_data')
    def test_produce_success(self, mock_produce_random_data, centrifugal_pump_controller):
        """Test the produce method when data is generated successfully."""
        # Arrange: Mock the return value of produce_random_data
        mock_registers = [mock.Mock(), mock.Mock()]  # Mocking two register objects
        mock_produce_random_data.return_value = mock_registers

        # Act: Call the produce method
        response = centrifugal_pump_controller.produce()

        # Assert: Check the response and the mock's behavior
        assert response[1] == 201  # The status code should be 201
        assert "message" in response[0].json
        assert len(response[0].json["data"]) == len(mock_registers)  # Check that data length matches

    @mock.patch('app.controllers.centrifugal_pump_controller.CentrifugalPumpRegisterService.produce_random_data')
    def test_produce_failure(self, mock_produce_random_data, centrifugal_pump_controller):
        """Test the produce method when an exception is raised."""
        # Arrange: Make produce_random_data raise an exception
        mock_produce_random_data.side_effect = Exception("Test error")

        # Act: Call the produce method
        response = centrifugal_pump_controller.produce()

        # Assert: Check the response for error handling
        assert response[1] == 500  # The status code should be 500
        assert "error" in response[0].json  # Ensure the error key is in the response
        assert "Internal Server Error" in response[0].json["message"]

    @mock.patch('app.adapters.producer.ProducerAdapter.start')
    def test_start_success(self, mock_start, centrifugal_pump_controller):
        """Test the start method when the producer starts successfully."""
        # Arrange: Mock the start method of ProducerAdapter
        mock_start.return_value = None

        # Act: Call the start method
        response = centrifugal_pump_controller.start()

        # Assert: Check that the response is as expected
        assert response[1] == 201  # The status code should be 201
        assert "result" in response[0].json
        assert response[0].json["result"] == "Producer starting to register actions from Centrifugal Pumps."

    @mock.patch('app.adapters.producer.ProducerAdapter.start')
    def test_start_failure(self, mock_start, centrifugal_pump_controller):
        """Test the start method when an exception occurs during starting."""
        # Arrange: Make the start method raise an exception
        mock_start.side_effect = Exception("Test error")

        # Act: Call the start method
        response = centrifugal_pump_controller.start()

        # Assert: Check the response for error handling
        assert response[1] == 500  # The status code should be 500
        assert "error" in response[0].json
        assert "Internal Server Error" in response[0].json["message"]

    @mock.patch('app.adapters.producer.ProducerAdapter.stop')
    def test_stop_success(self, mock_stop, centrifugal_pump_controller):
        """Test the stop method when the producer stops successfully."""
        # Arrange: Mock the stop method of ProducerAdapter
        mock_stop.return_value = "Producer service stopped."

        # Act: Call the stop method
        response = centrifugal_pump_controller.stop()

        # Assert: Check the response is as expected
        assert response[1] == 201  # The status code should be 201
        assert "result" in response[0].json
        assert response[0].json["result"] == "Producer service stopped."

    @mock.patch('app.adapters.producer.ProducerAdapter.stop')
    def test_stop_failure(self, mock_stop, centrifugal_pump_controller):
        """Test the stop method when an exception occurs during stopping."""
        # Arrange: Make stop method raise an exception
        mock_stop.side_effect = Exception("Test error")

        # Act: Call the stop method
        response = centrifugal_pump_controller.stop()

        # Assert: Check the response for error handling
        assert response[1] == 500  # The status code should be 500
        assert "error" in response[0].json
        assert "Internal Server Error" in response[0].json["message"]
