from flask import Flask, request, render_template, url_for, redirect, send_from_directory
from src.song_search.test import DeezerClient, logging
from splits.test import split_vocals_instrumentals  # Import the updated function
from src.visualisation.test import generate_waveform_with_slider
import os
import time
import re
import requests
from flask import jsonify

#Create a Flask app
app = Flask(__name__, static_folder="static", static_url_path="/static")

#Where music is saved
base_dir = os.path.dirname(os.path.abspath(__file__))
#Deezer client
cli = DeezerClient(base_dir)

#Directories for music in and out
MUSIC_IN_DIR = "/app/src/splits/music_in"
MUSIC_OUT_DIR = "/app/src/static/music_out"

#Home page
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    audio_url = None
    song_name = None
    tracks = None

    try:
        #Get the list of songs in music_in directory
        songs = [f for f in os.listdir(MUSIC_IN_DIR) if os.path.isfile(os.path.join(MUSIC_IN_DIR, f))]
        logging.info(f"Songs found in {MUSIC_IN_DIR}: {songs}")  # Debugging log
    except FileNotFoundError:
        logging.error(f"Directory {MUSIC_IN_DIR} not found.")
        songs = []  #assign an empty list

    #Handle POSTS
    if request.method == "POST":
        #Handle saving a song preview
        if "preview_url" in request.form and "name" in request.form:
            #Get the preview URL from the search
            preview_url = request.form.get("preview_url")
            track_name = request.form.get("name")  #Used to write filename
            music_dir = os.path.join(cli.base_dir, "splits/music_in")  #Where to save music
            try:
                #Ensure save dir exists
                os.makedirs(music_dir, exist_ok=True)
                response = requests.get(preview_url)
                #Unique timestamp per song
                preview_filename = f"preview_{track_name.replace(' ', '_')}_{int(time.time())}.mp3"
                #The actual path for preview of song
                preview_path = os.path.join(music_dir, preview_filename)
                logging.debug(f"Absolute path to saved file: {os.path.abspath(preview_path)}")
                #Save to dir
                with open(preview_path, "wb") as file:
                    file.write(response.content)
                    logging.debug(f"Preview saved to {preview_path}")
                return redirect(url_for('home'))
            except Exception as e:
                logging.debug(f"Connection error fetching preview: {e}")

        else:    
            #song search from search bar
            user_input = request.form.get("user_input")
            if user_input and user_input.strip():
                return redirect(url_for('home', search=user_input))
            return redirect(url_for('home'))
            
    search_query = request.args.get("search")
    if search_query:
        logging.info("Fetching tracks...")
        tracks = cli.loadSampleSong(search_query)  # Returns top 3 results
        
    #render the template with updated song list
    return render_template("home.html", tracks=tracks, songs=songs)

#edit page
@app.route("/edit", methods=["GET", "POST"])
def edit_page():
    #handle uploaded a mp3 file
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]

            if file.filename == "":
                return "No selected file"

            if file and file.filename.endswith(".mp3"):
                os.makedirs(MUSIC_IN_DIR, exist_ok=True)

                #Save the file to MUSIC_IN_DIR
                file_path = os.path.join(MUSIC_IN_DIR, file.filename)
                file.save(file_path)
                logging.info(f"File saved to {file_path}")

                #Redirect to edit page
                return redirect(url_for("edit_page"))

            return "Invalid file format. Only MP3 files are allowed."

        selected_song = request.form.get("song")
        if selected_song:
            #call the function to split the selected song and two directories
            split_vocals_instrumentals(MUSIC_IN_DIR, MUSIC_OUT_DIR, selected_song)
            return redirect(url_for('results_page', song=selected_song))
    #update song list
    songs = [f for f in os.listdir(MUSIC_IN_DIR) if os.path.isfile(os.path.join(MUSIC_IN_DIR, f))]
    return render_template("edit.html", songs=songs)
#results page
@app.route("/results")
def results_page():
    song = request.args.get("song")
    sanitized_song_name = re.sub(r'[^a-zA-Z0-9]', '_', os.path.splitext(song)[0])

    #5 graph splits
    vocals_file = f"music_out/{sanitized_song_name}/vocals.wav"
    drums_file = f"music_out/{sanitized_song_name}/drums.wav"
    bass_file = f"music_out/{sanitized_song_name}/bass.wav"
    other_file = f"music_out/{sanitized_song_name}/other.wav"
    piano_file = f"music_out/{sanitized_song_name}/piano.wav"

    #Render the template with the paths to the audio files
    return render_template("results.html", vocals_file=vocals_file, drums_file=drums_file,
                           bass_file=bass_file, other_file=other_file, piano_file=piano_file)
#Posts for graphs
@app.route('/vocal_graphs', methods=['POST'])
def handle_vocal_graph_request():
    data = request.get_json()
    app.logger.info(f"Received request data: {data}")
    filename = data.get('filename')
    #graph is json for Plotly
    if not filename:
        app.logger.error('No filename provided')
        return jsonify({'error': 'No filename provided'}), 400

    try:
        #add slider
        graph_json = generate_waveform_with_slider(filename)
        app.logger.info(f"Generated graph JSON: {graph_json}")
        return jsonify({'graph': graph_json})
    except Exception as e:
        app.logger.error(f"Error generating graph: {e}")
        return jsonify({'error': str(e)}), 500
@app.route('/drum_graphs', methods=['POST'])
def handle_drum_graph_request():
    data = request.get_json()
    app.logger.info(f"Received request data: {data}")
    filename = data.get('filename')
    if not filename:
        app.logger.error('No filename provided')
        return jsonify({'error': 'No filename provided'}), 400
    try:
        graph_json = generate_waveform_with_slider(filename)
        app.logger.info(f"Generated graph JSON: {graph_json}")
        return jsonify({'graph': graph_json})
    except Exception as e:
        app.logger.error(f"Error generating graph: {e}")
        return jsonify({'error': str(e)}), 500
@app.route('/bass_graphs', methods=['POST'])
def handle_bass_graph_request():
    data = request.get_json()
    app.logger.info(f"Received request data: {data}")
    filename = data.get('filename')
    if not filename:
        app.logger.error('No filename provided')
        return jsonify({'error': 'No filename provided'}), 400
    try:
        graph_json = generate_waveform_with_slider(filename)
        app.logger.info(f"Generated graph JSON: {graph_json}")
        return jsonify({'graph': graph_json})
    except Exception as e:
        app.logger.error(f"Error generating graph: {e}")
        return jsonify({'error': str(e)}), 500
@app.route('/other_graphs', methods=['POST'])
def handle_other_graph_request():
    data = request.get_json()
    app.logger.info(f"Received request data: {data}")
    filename = data.get('filename')
    if not filename:
        app.logger.error('No filename provided')
        return jsonify({'error': 'No filename provided'}), 400
    try:
        graph_json = generate_waveform_with_slider(filename)
        app.logger.info(f"Generated graph JSON: {graph_json}")
        return jsonify({'graph': graph_json})
    except Exception as e:
        app.logger.error(f"Error generating graph: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/piano_graphs', methods=['POST'])
def handle_piano_graph_request():
    data = request.get_json()
    app.logger.info(f"Received request data: {data}")
    filename = data.get('filename')
    if not filename:
        app.logger.error('No filename provided')
        return jsonify({'error': 'No filename provided'}), 400
    try:
        graph_json = generate_waveform_with_slider(filename)
        app.logger.info(f"Generated graph JSON: {graph_json}")
        return jsonify({'graph': graph_json})
    except Exception as e:
        app.logger.error(f"Error generating graph: {e}")
        return jsonify({'error': str(e)}), 500
#serve audio files
@app.route('/music_in/<path:filename>')
def serve_music_in(filename):
    return send_from_directory(MUSIC_IN_DIR, filename)
#localhost
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)