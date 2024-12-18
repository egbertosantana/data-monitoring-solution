import pytest
from unittest import mock
from app.services.centrifugal_pump_service import CentrifugalPumpService
from app.repository.centrifugal_pump_repository import CentrifugalPumpRepository
from app.models.centrifugal_pump import CentrifugalPump
from datetime import datetime

# Mocking CentrifugalPumpRepository
@pytest.fixture
def mock_repository():
    return mock.Mock(spec=CentrifugalPumpRepository)

@pytest.fixture
def centrifugal_pump_service(mock_repository):
    return CentrifugalPumpService()

class TestCentrifugalPumpService:

    @mock.patch('app.services.centrifugal_pump_service.CentrifugalPumpRepository', new_callable=mock.Mock)
    def test_map_pump_data(self, MockCentrifugalPumpRepository, centrifugal_pump_service):
        """Test that pump data is correctly mapped to a dictionary."""
        # Arrange: Create a mock pump object with necessary attributes
        pump = mock.Mock(spec=CentrifugalPump)
        pump.id = 1
        pump.maximum_temperature = 100
        pump.minimum_head = 5
        pump.maximum_head = 10
        pump.maximum_flow = 50
        pump.motor_voltage = 380
        pump.discharge_diameter = 10
        pump.suction_diameter = 8
        pump.impeller = 'Type-A'
        pump.impeller_material = 'Stainless Steel'
        pump.motor_frequency = 50
        pump.current_water_leak = 0.02
        pump.enabled = True
        pump.brand.name = 'BrandX'
        pump.created_at = datetime(2023, 1, 1)
        pump.updated_at = datetime(2023, 1, 2)

        # Act: Call the map_pump_data method
        mapped_data = centrifugal_pump_service.map_pump_data(pump)

        # Assert: Check that the returned dictionary has the correct keys and values
        assert mapped_data == {
            "id": 1,
            "maximum_temperature": 100,
            "minimum_head": 5,
            "maximum_head": 10,
            "maximum_flow": 50,
            "motor_voltage": 380,
            "discharge_diameter": 10,
            "suction_diameter": 8,
            "impeller": 'Type-A',
            "impeller_material": 'Stainless Steel',
            "motor_frequency": 50,
            "current_water_leak": 0.02,
            "enabled": True,
            "brand": 'BrandX',
            "created_at": '2023-01-01T00:00:00',
            "updated_at": '2023-01-02T00:00:00'
        }

    @mock.patch('app.services.centrifugal_pump_service.CentrifugalPumpRepository', new_callable=mock.Mock)
    def test_activate_pumps(self, MockCentrifugalPumpRepository, centrifugal_pump_service):
        """Test that all pumps are activated."""
        # Arrange: Mock the get_all method to return a list of pumps
        pump1 = mock.Mock(spec=CentrifugalPump)
        pump1.enabled = False
        pump2 = mock.Mock(spec=CentrifugalPump)
        pump2.enabled = False
        MockCentrifugalPumpRepository.get_all.return_value = [pump1, pump2]

        # Act: Call the activate_pumps method
        centrifugal_pump_service.activate_pumps()

        # Assert: Ensure that each pump's enabled attribute is set to True
        pump1.enabled = True
        pump2.enabled = True
        MockCentrifugalPumpRepository.add_all.assert_called_once_with([pump1, pump2])

    @mock.patch('app.services.centrifugal_pump_service.CentrifugalPumpRepository', new_callable=mock.Mock)
    def test_deactivate_pumps(self, MockCentrifugalPumpRepository, centrifugal_pump_service):
        """Test that all pumps are deactivated."""
        # Arrange: Mock the get_all method to return a list of pumps
        pump1 = mock.Mock(spec=CentrifugalPump)
        pump1.enabled = True
        pump2 = mock.Mock(spec=CentrifugalPump)
        pump2.enabled = True
        MockCentrifugalPumpRepository.get_all.return_value = [pump1, pump2]

        # Act: Call the deactivate_pumps method
        centrifugal_pump_service.deactivate_pumps()

        # Assert: Ensure that each pump's enabled attribute is set to False
        pump1.enabled = False
        pump2.enabled = False
        MockCentrifugalPumpRepository.add_all.assert_called_once_with([pump1, pump2])

    @mock.patch('app.services.centrifugal_pump_service.CentrifugalPumpRepository', new_callable=mock.Mock)
    def test_populate_pumps(self, MockCentrifugalPumpRepository, centrifugal_pump_service):
        """Test that the populate_pumps method is called."""
        # Arrange: Mock the populate_pumps method
        mock_populate_pumps = MockCentrifugalPumpRepository.populate_pumps

        # Act: Call the populate_pumps method
        centrifugal_pump_service.populate_pumps()

        # Assert: Ensure the populate_pumps method was called
        mock_populate_pumps.assert_called_once()
