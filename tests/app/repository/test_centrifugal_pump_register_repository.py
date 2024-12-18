import pytest
from unittest import mock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

@pytest.fixture
def mock_centrifugal_pump():
    """Fixture to mock a CentrifugalPump object."""
    from app.models.centrifugal_pump import CentrifugalPump
    pump = mock.Mock(spec=CentrifugalPump)
    pump.enabled = True
    pump.id = 1
    return pump


@pytest.fixture
def mock_centrifugal_pump_register():
    """Fixture to mock a CentrifugalPumpRegister object."""
    from app.models.centrifugal_pump_register import CentrifugalPumpRegister
    register = mock.Mock(spec=CentrifugalPumpRegister)
    return register


class TestCentrifugalPumpRegisterRepository:
    @mock.patch('app.models.centrifugal_pump.CentrifugalPump.query.filter_by')
    def test_get_all_enabled_pumps(self, mock_filter_by, mock_centrifugal_pump):
        """Test get_all_enabled_pumps method."""
        from app.repository.centrifugal_pump_register_repository import CentrifugalPumpRegisterRepository
        # Arrange
        mock_filter_by.return_value.all.return_value = [mock_centrifugal_pump]
        
        # Act
        pumps = CentrifugalPumpRegisterRepository.get_all_enabled_pumps()
        
        # Assert
        mock_filter_by.assert_called_once_with(enabled=True)
        mock_filter_by.return_value.all.assert_called_once()
        assert len(pumps) == 1
        assert pumps[0] == mock_centrifugal_pump

    @mock.patch('app.adapters.database.db.session.add_all')
    @mock.patch('app.adapters.database.db.session.commit')
    def test_add_registers(self, mock_commit, mock_add_all, mock_centrifugal_pump_register):
        """Test add_registers method."""
        # Arrange
        from app.repository.centrifugal_pump_register_repository import CentrifugalPumpRegisterRepository
        registers = [mock_centrifugal_pump_register]
        
        # Act
        CentrifugalPumpRegisterRepository.add_registers(registers)
        
        # Assert
        mock_add_all.assert_called_once_with(registers)
        mock_commit.assert_called_once()

    @mock.patch('app.adapters.database.db.session.add')
    @mock.patch('app.adapters.database.db.session.commit')
    def test_update_pump(self, mock_commit, mock_add, mock_centrifugal_pump):
        """Test update_pump method."""
        # Arrange
        pump = mock_centrifugal_pump
        
        # Act
        from app.repository.centrifugal_pump_register_repository import CentrifugalPumpRegisterRepository
        CentrifugalPumpRegisterRepository.update_pump(pump)
        
        # Assert
        mock_add.assert_called_once_with(pump)
        mock_commit.assert_called_once()
