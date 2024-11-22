import re
import os
from flask import Flask, render_template, request, redirect, url_for
from deezer.test import split_vocals_instrumentals  

# Create a Flask application
app = Flask(__name__)


MUSIC_IN_DIR = "/app/src/deezer/music_in"
MUSIC_OUT_DIR = "/app/src/static/music_out" 

# Define a route
@app.route("/")
def home():
    return render_template("home.html")

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
