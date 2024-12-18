import pytest
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Mocking db session methods for unit testing
@pytest.fixture
def mock_db_session():
    with patch('app.adapters.database.db.session') as mock_session:
        yield mock_session

# Mocking the CentrifugalPump model
@pytest.fixture
def mock_centrifugal_pump_model():
    with patch('app.models.centrifugal_pump.CentrifugalPump') as mock_model:
        yield mock_model

# Mocking the Brand model
@pytest.fixture
def mock_brand_model():
    with patch('app.models.brand.Brand') as mock_model:
        yield mock_model

def test_get_all_pumps(mock_db_session, mock_centrifugal_pump_model):
    # Setup mock return value for query.all()
    from app.repository.centrifugal_pump_repository import CentrifugalPumpRepository
    mock_centrifugal_pump_model.query.all.return_value = ['pump1', 'pump2', 'pump3']
    
    # Call the method to test
    pumps = CentrifugalPumpRepository.get_all()

    # Assert that the correct method was called and the expected result was returned
    mock_centrifugal_pump_model.query.all.assert_called_once()
    assert pumps == ['pump1', 'pump2', 'pump3']

def test_get_by_brand_id(mock_db_session, mock_centrifugal_pump_model, mock_brand_model):
    # Setup mock return value for filter_by().first()
    from app.repository.centrifugal_pump_repository import CentrifugalPumpRepository
    mock_centrifugal_pump_model.query.filter_by.return_value.first.return_value = 'pump1'
    
    # Call the method to test
    pump = CentrifugalPumpRepository.get_by_brand_id(1)

    # Assert that the correct method was called and the expected result was returned
    mock_centrifugal_pump_model.query.filter_by.assert_called_once_with(brand_id=1)
    mock_centrifugal_pump_model.query.filter_by.return_value.first.assert_called_once()
    assert pump == 'pump1'

def test_add_all_pumps(mock_db_session, mock_centrifugal_pump_model):
    # Create a list of mock pumps
    from app.repository.centrifugal_pump_repository import CentrifugalPumpRepository
    pumps = ['pump1', 'pump2', 'pump3']

    # Call the method to test
    CentrifugalPumpRepository.add_all(pumps)

    # Assert that db.session.add_all and db.session.commit were called
    mock_db_session.add_all.assert_called_once_with(pumps)
    mock_db_session.commit.assert_called_once()

def test_populate_pumps(mock_db_session, mock_centrifugal_pump_model, mock_brand_model):
    # Mock random.choice for the impeller type and material
    with patch('random.choice', side_effect=['Closed', 'Stainless Steel', 220, 50.0]):
        from app.models.brand import Brand
        # Mock Brand entity and its return values
        mock_brand = MagicMock(spec=Brand)
        mock_brand.id = 1
        mock_brand.name = 'Ferrari'
        mock_brand_model.query.filter_by.return_value.first.return_value = mock_brand

        # Call the method to test
        from app.repository.centrifugal_pump_repository import CentrifugalPumpRepository
        CentrifugalPumpRepository.populate_pumps()

        # Assert that the repository methods were called
        mock_brand_model.query.filter_by.return_value.first.assert_called_once_with(name='Ferrari')
        mock_centrifugal_pump_model.assert_called_once()

        # Check if add_all method was called with the pumps list
        mock_db_session.add_all.assert_called_once()

        # Ensure that the proper print statement is executed (or mocked)
        # In real test, you can assert the print output if necessary, but here we assume it worked.
