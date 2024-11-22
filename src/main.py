from flask import Flask, request, render_template_string, url_for, send_from_directory
from src.spotipy.test import SpotipyClient, logging
import os

app = Flask(__name__, static_folder="music",static_url_path="/")

#Spotipy class and dir so we know where to save music
base_dir = os.path.dirname(os.path.abspath(__file__))
sp = SpotipyClient(base_dir)

#HTML template for the form
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Input Form</title>
</head>
<body>
    <h1>Search Artist</h1>
        <form method="post" action="/">
            <label for="user_input">Input:</label>
            <input type="text" id="user_input" name="user_input">
            <button type="submit">Submit</button>
        </form>

    {% if result %}
    <h2>Search Result: {{ result }}</h2>
    {% endif %}
    {% if audio_url %}
        <!-- Audio player is displayed -->
        <p>Audio URL: {{ audio_url }}</p>
        <audio controls>
            <source src="{{ audio_url }}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    {% else %}
        <!-- Message displayed if file doesn't exist -->
        <p>No audio file available to play.</p>
    {% endif %}

    <script>
        console.log("Script loaded successfully!");
        function handleSubmit(event, inputId) {
            event.preventDefault(); // Prevent page reload
            // Example JavaScript logic (optional)
            const userInput = document.getElementById(inputId).value; // Get input value
            console.log("Input value submitted:", userInput);
            return true; // Proceed with form submission
        }
    </script>
</body>
</html>
"""
#home page post route and fetch route for preview
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    audio_url = None
    if request.method == "POST":
        #Retrieve song search
        user_input = request.form.get("user_input")
        logging.info("Attempting to connect to Spotipy...")
        sp.connectToSpotipy()  #connect

        result = f"Connected to Spotipy with query: {user_input}"  #debug html
        logging.info("Writing song...")
        saved_file = sp.loadSampleSong(user_input)  # Returns the unique filename
        file_path = os.path.join(app.static_folder, saved_file)
        if os.path.exists(file_path): #try serve mp3 preview
        # Generate a URL to serve the file
            audio_url = url_for("static", filename=saved_file)
            logging.info(f"Audio file URL: {audio_url}")
        else:
            audio_url = None
            logging.warning(file_path)
            logging.warning("Audio file not found.")

    return render_template_string(HTML_TEMPLATE, audio_url=audio_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
