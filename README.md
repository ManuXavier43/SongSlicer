# Song Slicer

Song slicer is a python application proposal that allows you to slice songs to separate vocals and instruments by category. We're developing this so people can easily create tracks with their favourite instruments, isolate vocals or even make a karaoke version for a night out!

# Sprint timeline

+ Week 1: Set up Spotipy to fetch song samples and group song data
+ Week 2: Edit Screen UI, split a song into one category, generate a spectrogram on a sample song
+ Week 3: Add sliders for frequency etc, split a song into different categories, intergrate spectrogram for different instruments and with slider
+ Week 4: Design home page, add spotify songs to home page, connect to spotify profile in app
+ Week 5: Saving track functionality in app, search songs by name, comparisions of graphs of different splits (possibly generate insights).

# Intro

This project is a Flask app that uses the Deezer Spleeter to split songs into vocals and instrumentals. For demo purposes, previews can be fetched using the Spotify api.

## Run Flask app using Docker

```docker build -t song-slicer .  ```
```docker run -p 8080:5000 song-slicer``` This maps the container port 5000 to local port 8080

**Flask container URL:** http://127.0.0.1:8080/

# (DEBUGGING) Run python app using Docker

```docker build -t song-slicer .  ```
```docker run -it song-slicer /bin/bash```
```python src/[PATH_TO_PYTHON_FILE]```

# Docker Dependencies
Previously, this project made use of a virtual conda "spleeter" env with py -v 3.8 as spleeter has deprecated dependancies.
"conda activate spleeter-env"

We decided to switch to a dockerfile that handles all the dependencies for this project so it no longer relies on an Anaconda environment. Here are some of the libraries we're using in our ```requirements.txt``` file.

**Deezer:** 
Previously samples were sourced from Spotify. Spotify made API changes so we switched to Deezer API. The app fetches 30 second samples from deezer API link. They are saved to the ```music_in``` folder.

**Spleeter**
Spleeter is used to isolate the source track into vocals, instrumentals, etc.

**Flask**
Song-Slicer is built using Flask for its GUI. It handles POST and GET requests. Tracks are served using different routes and there's mainly a home, edit and results page.
