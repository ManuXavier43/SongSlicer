from flask import Flask, request, render_template, url_for, redirect, send_from_directory
from src.song_search.test import DeezerClient, logging
from splits.test import split_vocals_instrumentals
import os, time
import re
import requests
from visualisation.test import generate_waveform_with_slider
from flask import jsonify

# Create a Flask application
app = Flask(__name__, static_folder="static", static_url_path="/static")

# Spotipy class and dir so we know where to save music
base_dir = os.path.dirname(os.path.abspath(__file__))
cli = DeezerClient(base_dir)

MUSIC_IN_DIR = "/app/src/splits/music_in"
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
        if "preview_url" in request.form and "name" in request.form:
            # Get the preview URL from the form
            preview_url = request.form.get("preview_url")
            track_name = request.form.get("name") #Used to write filename
            music_dir = os.path.join(cli.base_dir, "splits/music_in") #Where to save music
            try:
                #ensure save dir exists
                os.makedirs(music_dir, exist_ok=True)
                #get song
                response = requests.get(preview_url)
                #unique timestamp per song
                preview_filename = f"preview_{track_name.replace(' ', '_')}_{int(time.time())}.mp3"
                #actual path for preview
                preview_path = os.path.join(music_dir, preview_filename)
                logging.debug(f"Absolute path to saved file: {os.path.abspath(preview_path)}")
                #save to dir
                with open(preview_path, "wb") as file:
                    file.write(response.content)
                    logging.debug(f"Preview saved to {preview_path}")
                    #only return filename as html knows the static folder
                    # return f"Song saved as {preview_filename}"
                return redirect(url_for('home'))
            except Exception as e:
                logging.debug(f"Connection error fetching preview: {e}")

        else:    
            # Retrieve song search
            user_input = request.form.get("user_input")
            if user_input and user_input.strip():
                return redirect(url_for('home', search=user_input))
            return redirect(url_for('home'))
            
    search_query = request.args.get("search")
    if search_query:
        # logging.info("Attempting to connect to Spotipy...")
        # cli.connectToSpotipy()  # Connect
        logging.info("Fetching tracks...")
        tracks = cli.loadSampleSong(search_query)  # Returns top 3 results
        
    # Render the template with updated song list
    return render_template("home.html", tracks=tracks, songs=songs)

# Save button route for any of the top 3 songs

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

@app.route('/vocal_graphs', methods=['POST'])
def handle_vocal_graph_request():
    data = request.get_json()
    app.logger.info(f"Received request data: {data}")
    filename = data.get('filename')
    if not filename:
        app.logger.error('No filename provided')
        return jsonify({'error': 'No filename provided'}), 400

    try:
        # Generate graph
        graph_json = generate_waveform_with_slider(filename)
        app.logger.info(f"Generated graph JSON: {graph_json}")
        return jsonify({'graph': graph_json})
    except Exception as e:
        app.logger.error(f"Error generating graph: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/accompaniment_graphs', methods=['POST'])
def handle_acc_graph_request():
    filename = request.json.get('filename')  # Fetch JSON data from request
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    logging.info(f"Received request to generate accompaniment graph for {filename}")
    
    # Generate the waveform
    graph_json = generate_waveform_with_slider(filename)
    
    return jsonify({'graph': graph_json})  # Return JSON response

@app.route('/music_in/<path:filename>')
def serve_music_in(filename):
    return send_from_directory(MUSIC_IN_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
