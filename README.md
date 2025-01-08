# Song-Slicer

Song-Slicer is a python application proposal that allows you to slice songs to separate vocals and instruments by category. We're developing this so people can easily create tracks with their favourite instruments, isolate vocals or even make a karaoke version for a night out!

# Initial Sprint Timeline for first few weeks...

+ Week 1: Set up Spotipy to fetch song samples and group song data
+ Week 2: Edit Screen UI, split a song into one category, generate a spectrogram on a sample song
+ Week 3: Add sliders for frequency etc, split a song into different categories, intergrate spectrogram for different instruments and with slider
+ Week 4: Design home page, add spotify songs to home page, connect to spotify profile in app
+ Week 5: Saving track functionality in app, search songs by name, comparisions of graphs of different splits (possibly generate insights).

# Actual Sprint Timeline
+ Week 1: Connected to Spotipy and could get a live song feed from the user.
+ Week 2: Fetched a set of tracks from Spotipy. Set up a virtual anaconda environment for dependencies.
+ Week 3: Deezer Spleeter program could split a local file into 2 stems. User input added for Spotipy searching of tracks.
+ Week 4: Changed to docker environment from anaconda. Created a dockerfile for Song-Slicer. Set up Flask. Created Home , edit and results page templates. Connected the Spleeter and Spotipy classes. The user could now search a Spotipy sample on the home page, navigate to edit page to choose which song to split, split it with Deezer and have the result shown in the results page with audio player.
+ Week 5: Spotify changed their TOS for their API so we switched to Deezer for fetching song samples. Changed the logic to fetch Deezer tracks instead.
+ Week 6: Changed Spleeter from 2 stems to 5 stems for 5 splits. Researched APIs for song cleanup. UI overall, especially on results page.
+ Week 7: Added Plotly graph buttons for each split on the results page for amplitude over time. A resultion slider was added to see the waves in more or less detail.
+ Week 8: Researched and experimented with hosting Song-Slicer on Azure rather than localhost. Created a virtual machine in Azure to experiment with connecting to an IP address hosting the app, but decided against it due to time constraints and no content moderation.

# Intro

This project is a Flask app that uses the Deezer Spleeter to split songs into vocals and instrumentals. For demo purposes, previews can be fetched using the Deezer api, however local mp3 files can also be uploaded for splitting. Plotly is used to display waveforms of each split, showing the split's amplitude over time.

## Install Docker Desktop

https://www.docker.com/products/docker-desktop/

## Run Flask app using Docker

Navigate to the inner song-slicer-main directory ```song-slicer-main\song-slicer-main```. This parent directory should be a level above the Dockerfile, the src folder, the README etc.
```docker build -t song-slicer .  ```
```docker run -p 8080:5000 song-slicer``` This maps the container port 5000 to local port 8080

**Flask container URL:** Access the website on localhost: http://127.0.0.1:8080/
In case the Deezer API takes some time to respond on the first startup, stop the container and run again.

# (DEBUGGING) Run python app using Docker

```docker build -t song-slicer .  ```
```docker run -it song-slicer /bin/bash```
```python src/[PATH_TO_PYTHON_FILE]```

# TESTING Song-Slicer
```docker build -t song-slicer-test .  ```
```docker run --rm song-slicer-test```

# Primary Docker Dependencies
Previously, this project made use of a virtual conda "spleeter" env with py -v 3.8 as spleeter has deprecated dependancies.
"conda activate spleeter-env"

We decided to switch to a dockerfile that handles all the dependencies for this project so it no longer relies on an Anaconda environment. Here are some of the libraries we're using in our ```requirements.txt``` file.

**Deezer:** 
Previously samples were sourced from Spotify. Spotify made API changes so we switched to Deezer API. The app fetches 30 second samples from deezer API link. They are saved to the ```music_in``` folder.

**Spleeter**
Spleeter is used to isolate the source track into vocals, instrumentals, etc.

**Flask**
Song-Slicer is built using Flask for its GUI. It handles POST and GET requests. Tracks are served using different routes and there's a home, edit and results page.

**Plotly**
Plotly is used to display waveforms of each respective split.

**PyTest**
PyTest is used for 14 unit tests that test Song-Slicer routes and splitting functionalities.

# Secondary Docker Dependencies

**Werkzeug**
Security dependency for Flask

**Numpy**
To generate waveform signal

**Scipy**
TO change amplitude level of detail using the resample method

**Tensorflow/Tensorflow-CPU**
Dependency of Spleeter for creating song splits using GPU/CPU respectively