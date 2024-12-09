import wave as wv  # To open wav files
import numpy as np  # To analyze audio bits
import plotly.graph_objects as go  # To plot a frequency graph
from flask import jsonify #handle graph as json

def generate_waveform(sanitized_song_name):
    vocals_file = f"/app/src/static/{sanitized_song_name}"
    
    # Open the audio file
    song = wv.open(vocals_file, 'rb')
    freq = song.getframerate()  # Get the frequency of the audio
    samples = song.getnframes()  # Number of samples
    t = samples / freq  # Time duration in seconds
    nchannels = song.getnchannels()

    print(
        f"Frequency: {freq} Hz",
        f"Samples: {samples}",
        f"Time: {t} seconds",
        f"Number channels: {nchannels}",
        sep='\n'
    )

    # Read signal and convert to numpy array
    signal = np.frombuffer(song.readframes(samples), dtype=np.int16)
    song.close()

    # Generate time axis
    time_axis = np.linspace(0, t, num=samples)

    # Plot the waveform
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_axis, y=signal, mode='lines', name='Waveform'))
    fig.update_layout(
        title="Waveform",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
        template="plotly_white"
    )

    # Display the plot
    fig.show()
    fig_json = fig.to_json()
    return fig_json
