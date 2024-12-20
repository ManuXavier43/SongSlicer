import pytest
from unittest.mock import patch
import os, sys
# Debug the current working directory
print("Current working directory:", os.getcwd())

# Debug the Python path
print("PYTHONPATH:", sys.path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.main import app  # Assuming the Flask app is in app.py

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch("src.main.cli.loadSampleSong")
def test_home_search_query(mock_loadSampleSong, client):
    # Mock the search functionality to return dummy results
    mock_loadSampleSong.return_value = [{"name": "Sample Song", "preview_url": "http://example.com"}]
    
    # Simulate a GET request with a search query
    response = client.get("/?search=test")
    
    # Assertions
    assert response.status_code == 200
    assert b"Sample Song" in response.data  # Check that the song name is in the response
    mock_loadSampleSong.assert_called_once_with("test")  # Ensure the correct query is passed
