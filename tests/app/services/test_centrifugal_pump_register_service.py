import pytest
from unittest import mock
from app.services.centrifugal_pump_register_service import CentrifugalPumpRegisterService
from app.repository.centrifugal_pump_register_repository import CentrifugalPumpRegisterRepository
from app.models.centrifugal_pump_register import CentrifugalPumpRegister
from datetime import datetime

# Mocking CentrifugalPumpRegisterRepository
@pytest.fixture
def mock_repository():
    return mock.Mock(spec=CentrifugalPumpRegisterRepository)

@pytest.fixture
def centrifugal_pump_register_service(mock_repository):
    return CentrifugalPumpRegisterService()

class TestCentrifugalPumpRegisterService:

    @mock.patch('app.services.centrifugal_pump_register_service.CentrifugalPumpRegisterRepository', new_callable=mock.Mock)
    def test_produce_random_data(self, MockCentrifugalPumpRegisterRepository, centrifugal_pump_register_service):
        """Test that random data is generated and added to the database."""
        # Arrange
        mock_repository = MockCentrifugalPumpRegisterRepository.return_value
        mock_repository.get_all_enabled_pumps.return_value = [mock.Mock(id=1, current_water_leak=0.01)]
        mock_register = mock.Mock(spec=CentrifugalPumpRegister)

        # Act
        generated_registers = centrifugal_pump_register_service.produce_random_data()

        # Assert
        mock_repository.get_all_enabled_pumps.assert_called_once()  # Ensure pumps were queried
        mock_repository.update_pump.assert_called_once()  # Ensure pump was updated
        mock_repository.add_registers.assert_called_once()  # Ensure registers were added
        assert len(generated_registers) > 0  # Should return at least one register
        assert isinstance(generated_registers[0], CentrifugalPumpRegister)  # Check that the generated data is of the correct type

    @mock.patch('app.services.centrifugal_pump_register_service.CentrifugalPumpRegisterRepository', new_callable=mock.Mock)
    def test_no_enabled_pumps(self, MockCentrifugalPumpRegisterRepository, centrifugal_pump_register_service):
        """Test that no data is generated when there are no enabled pumps."""
        # Arrange
        mock_repository = MockCentrifugalPumpRegisterRepository.return_value
        mock_repository.get_all_enabled_pumps.return_value = []  # No enabled pumps

        # Act
        generated_registers = centrifugal_pump_register_service.produce_random_data()

        # Assert
        mock_repository.get_all_enabled_pumps.assert_called_once()  # Ensure pumps were queried
        mock_repository.update_pump.assert_not_called()  # No pumps should be updated
        mock_repository.add_registers.assert_not_called()  # No registers should be added
        assert generated_registers == []  # Should return an empty list

    @mock.patch('app.services.centrifugal_pump_register_service.CentrifugalPumpRegisterRepository', new_callable=mock.Mock)
    def test_generate_random_data_correctness(self, MockCentrifugalPumpRegisterRepository, centrifugal_pump_register_service):
        """Test that the generated random data falls within expected ranges."""
        # Arrange
        mock_repository = MockCentrifugalPumpRegisterRepository.return_value
        mock_repository.get_all_enabled_pumps.return_value = [mock.Mock(id=1, current_water_leak=0.01)]
        mock_register = mock.Mock(spec=CentrifugalPumpRegister)

        # Act
        generated_registers = centrifugal_pump_register_service.produce_random_data()

        # Assert: Check that the generated values fall within expected ranges
        assert 10.0 <= generated_registers[0].energy_consumption <= 100.0
        assert 5.0 <= generated_registers[0].flow_rate <= 50.0
        assert 20.0 <= generated_registers[0].temperature <= 80.0
        assert 0.1 <= generated_registers[0].vibration <= 5.0
        assert 0.0 <= generated_registers[0].moment_water_leak <= 0.01

    @mock.patch('app.services.centrifugal_pump_register_service.CentrifugalPumpRegisterRepository', new_callable=mock.Mock)
    @mock.patch('app.services.centrifugal_pump_register_service.logger')
    def test_warning_when_no_pumps(self, mock_logger, MockCentrifugalPumpRegisterRepository, centrifugal_pump_register_service):
        """Test that a warning is logged when no enabled pumps are found."""
        # Arrange
        mock_repository = MockCentrifugalPumpRegisterRepository.return_value
        mock_repository.get_all_enabled_pumps.return_value = []  # No enabled pumps

        # Act
        centrifugal_pump_register_service.produce_random_data()

        # Assert
        mock_logger.warning.assert_called_once_with("No enabled pumps found in the database.")

    @mock.patch('app.services.centrifugal_pump_register_service.CentrifugalPumpRegisterRepository', new_callable=mock.Mock)
    def test_generate_and_update_pumps(self, MockCentrifugalPumpRegisterRepository, centrifugal_pump_register_service):
        """Test that pumps are updated correctly after random data is generated."""
        # Arrange
        pump = mock.Mock(id=1, current_water_leak=0.01)
        mock_repository = MockCentrifugalPumpRegisterRepository.return_value
        mock_repository.get_all_enabled_pumps.return_value = [pump]

        # Act
        centrifugal_pump_register_service.produce_random_data()

        # Assert: Ensure the pump was updated with new water leak value
        pump.updated_at = datetime.now()  # mock the updated timestamp
        mock_repository.update_pump.assert_called_once_with(pump)  # Ensure that pump is updated
