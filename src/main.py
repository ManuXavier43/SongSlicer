from flask import Flask, request, render_template, render_template_string, url_for, send_from_directory
from src.spotipy.test import SpotipyClient, logging
import os

# Create a Flask application
app = Flask(__name__, static_folder="deezer/music_in",static_url_path="/")
#Spotipy class and dir so we know where to save music
base_dir = os.path.dirname(os.path.abspath(__file__))
sp = SpotipyClient(base_dir)
# Define a route
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    audio_url = None
    song_name = None
    tracks = None
    if request.method == "POST":
        #Retrieve song search
        user_input = request.form.get("user_input")
        logging.info("Attempting to connect to Spotipy...")
        sp.connectToSpotipy()  #connect

        result = f"Connected to Spotipy with query: {user_input}"  #debug html
        logging.info("Writing song...")
        saved_file,tracks = sp.loadSampleSong(user_input)  # Returns the unique filename
        file_path = os.path.join(app.static_folder, saved_file)
        if os.path.exists(file_path) and tracks: #try serve mp3 preview
        # Generate a URL to serve the file
            audio_url = url_for("static", filename=saved_file)
            logging.info(f"Audio file URL: {audio_url}")
        else:
            audio_url = None
            logging.warning(file_path)
            logging.warning("Audio file not found.")
    return render_template("home.html",audio_url=audio_url,tracks=tracks)

@app.route("/edit")
def edit_page():
    return render_template("edit.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


