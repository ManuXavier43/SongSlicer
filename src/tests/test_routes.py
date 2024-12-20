from io import BytesIO
import pytest, flask
from flask import url_for
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

#Test that pages load
def test_home_page_load(client):
        # Test the home route
        response = client.get("/")
        assert response.status_code == 200

def test_edit_page_load(client):
        # Test the edit route
        response = client.get("/edit")
        assert response.status_code == 200

def test_home_page_post(client):
        # Test the home route redirects on POST
        response = client.post("/")
        assert response.status_code == 302
        assert response.location == url_for('home', _external=True)

class TestEditPage:
    @patch("os.makedirs")  # Mock os.makedirs to avoid creating directories during testing
    @patch("os.path.isfile", return_value=False)  # Mock os.path.isfile to simplify file checks
    @patch("os.listdir", return_value=["test_song.mp3"])  # Mock os.listdir to simulate songs
    def test_valid_mp3_upload(self, mock_listdir, mock_isfile, mock_makedirs, client):
        # Simulate uploading a valid MP3 file
        data = {
            "file": (BytesIO(b"fake mp3 content"), "test_song.mp3")
        }
        response = client.post("/edit", data=data, content_type="multipart/form-data")

        # Assert redirect after successful upload
        assert response.status_code == 302
        assert response.location == url_for('edit_page', _external=True)

    @patch("os.makedirs")
    def test_invalid_file_upload(self, mock_makedirs, client):
        # Simulate uploading an invalid file format
        data = {
            "file": (BytesIO(b"fake content"), "invalid_file.txt")
        }
        response = client.post("/edit", data=data, content_type="multipart/form-data")

        # Assert response with an error message
        assert response.status_code == 200
        # assert b"Invalid file format. Only MP3 files are allowed." in response.data

    @patch("os.makedirs")
    def test_no_file_selected(self, mock_makedirs, client):
        # Simulate submitting the form with no file
        data = {}
        response = client.post("/edit", data=data, content_type="multipart/form-data")

        # Assert response with an error message
        assert response.status_code == 200
        # assert b"No selected file" in response.data

#Graphs
def test_results_page(client):
    response = client.get("/results?song=test_song.mp3")
    selected_song = "test_song.mp3"
    assert response.status_code == 200
    assert url_for('results_page', song=selected_song)
def test_vocal_graphs(client):
    data = {"filename": "test_vocals.wav"}
    response = client.post("/vocal_graphs", json=data)
    assert response.status_code == 200
    assert "graph" in response.json
def test_drum_graphs(client):
    data = {"filename": "test_drums.wav"}
    response = client.post("/drum_graphs", json=data)
    assert response.status_code == 200
    assert "graph" in response.json
def test_bass_graphs(client):
    data = {"filename": "test_bass.wav"}
    response = client.post("/bass_graphs", json=data)
    assert response.status_code == 200
    assert "graph" in response.json
def test_other_graphs(client):
    data = {"filename": "test_other.wav"}
    response = client.post("/other_graphs", json=data)
    assert response.status_code == 200
    assert "graph" in response.json
def test_piano_graphs(client):
    data = {"filename": "test_piano.wav"}
    response = client.post("/piano_graphs", json=data)
    assert response.status_code == 200
    assert "graph" in response.json

#Test Spleeter
class TestSpleet:
    @patch("src.main.split_vocals_instrumentals")
    def test_split_song_functionality(self, mock_split, client):
        # Step 1: Prepare POST data
        data = {"song": "test_song.mp3"}
        print("POST data:", data)

        # Step 2: Send POST request
        response = client.post("/edit", data=data)
        print("Response status code:", response.status_code)
        print("Response location:", response.location)

        # Step 3: Verify status code
        assert response.status_code == 302, f"Expected 302, got {response.status_code}"

        # Step 4: Verify redirection URL
        expected_location = url_for('results_page', song="test_song.mp3", _external=True)
        assert response.location == expected_location, f"Expected location {expected_location}, got {response.location}"

        # Step 5: Verify split function call
        print("Mock split call args:", mock_split.call_args_list)
        mock_split.assert_called_once_with("/app/src/splits/music_in", "/app/src/static/music_out", "test_song.mp3")
