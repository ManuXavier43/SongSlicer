from flask import Flask, request, render_template, url_for, redirect, send_from_directory
from src.spotipy.test import SpotipyClient, logging
from deezer.test import split_vocals_instrumentals
import os
import re

# Create a Flask application
app = Flask(__name__, static_folder="static", static_url_path="/static")

# Spotipy class and dir so we know where to save music
base_dir = os.path.dirname(os.path.abspath(__file__))
sp = SpotipyClient(base_dir)

MUSIC_IN_DIR = "/app/src/deezer/music_in"
MUSIC_OUT_DIR = "/app/src/static/music_out"

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    audio_url = None
    song_name = None
    tracks = None
    
    try:
        # Get the list of songs in music_in directory
        songs = [f for f in os.listdir(MUSIC_IN_DIR) if os.path.isfile(os.path.join(MUSIC_IN_DIR, f))]
        logging.info(f"Songs found in {MUSIC_IN_DIR}: {songs}")  # Debugging log
    except FileNotFoundError:
        logging.error(f"Directory {MUSIC_IN_DIR} not found.")
        songs = []  # Handle missing directory by assigning an empty list

    if request.method == "POST":
        # Retrieve song search
        user_input = request.form.get("user_input")
        logging.info("Attempting to connect to Spotipy...")
        sp.connectToSpotipy()  # Connect

        result = f"Connected to Spotipy with query: {user_input}"  # Debug HTML
        logging.info("Writing song...")
        saved_file, tracks = sp.loadSampleSong(user_input)  # Returns the unique filename
        file_path = os.path.join(app.static_folder, saved_file)
        if os.path.exists(file_path) and tracks:  # Try to serve mp3 preview
            # Generate a URL to serve the file
            audio_url = url_for("static", filename=saved_file)
            logging.info(f"Audio file URL: {audio_url}")
        else:
            audio_url = None
            logging.warning(file_path)
            logging.warning("Audio file not found.")

    # Render the template with updated song list
    return render_template("home.html", audio_url=audio_url, tracks=tracks, songs=songs)

@app.route("/edit", methods=["GET", "POST"])
def edit_page():
    songs = [f for f in os.listdir(MUSIC_IN_DIR) if os.path.isfile(os.path.join(MUSIC_IN_DIR, f))]

    if request.method == "POST":
        selected_song = request.form.get("song")
        if selected_song:
            # Call the function to split the selected song with the correct arguments
            split_vocals_instrumentals(MUSIC_IN_DIR, MUSIC_OUT_DIR, selected_song)
            return redirect(url_for('results_page', song=selected_song))

    return render_template("edit.html", songs=songs)

@app.route("/results")
def results_page():
    song = request.args.get("song")
    sanitized_song_name = re.sub(r'[^a-zA-Z0-9]', '_', os.path.splitext(song)[0])

    # Update paths to match where files are actually saved in the static directory
    vocals_file = f"music_out/{sanitized_song_name}/vocals.wav"
    accompaniment_file = f"music_out/{sanitized_song_name}/accompaniment.wav"

    # Render the template with the paths to the audio files
    return render_template("results.html", vocals_file=vocals_file, accompaniment_file=accompaniment_file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
