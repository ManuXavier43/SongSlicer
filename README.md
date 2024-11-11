# Song Slicer

Song slicer is a python application proposal that allows you to slice songs to separate vocals and instruments by category. We're developing this so people can easily create tracks with their favourite instruments, isolate vocals or even make a karaoke version for a night out!

# Sprint timeline

+ Week 1: Set up Spotipy to fetch song samples and group song data
+ Week 2: Edit Screen UI, split a song into one category, generate a spectrogram on a sample song
+ Week 3: Add sliders for frequency etc, split a song into different categories, intergrate spectrogram for different instruments and with slider
+ Week 4: Design home page, add spotify songs to home page, connect to spotify profile in app
+ Week 5: Saving track functionality in app, search songs by name, comparisions of graphs of different splits (possibly generate insights).

# Setup

This project is a Python based audio splitter appilcation that uses pip libraries.

## Dependencies

**Spotipy:** 
pip install spotipy
Song samples are sourced from Spotify

**CustomTKinter**
pip install customtkinter
CustomTKinter is our app GUI

The following libraries are for audio analysis and plotting waveforms
**MatplotLib**
pip install matplotlib

**Numpy**
pip install numpy

## Classes

+ ```song-slicer\src\spotipy\test.py``` connects to your Spotify account and plays your saved library
+ ```song-slicer\src\main.py``` Draws app