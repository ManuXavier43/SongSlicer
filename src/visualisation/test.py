import wave as wv
import numpy as np
import plotly.graph_objects as go
import json
from scipy.signal import resample

def generate_waveform_with_slider(sanitized_song_name):
    print("Starting waveform generation...")
    vocals_file = f"/app/src/static/{sanitized_song_name}"
    print(f"Processing file: {vocals_file}")

    #Open the audio file
    try:
        song = wv.open(vocals_file, 'rb')
        freq = song.getframerate()  #Original sampling frequency
        samples = song.getnframes()  #Number of samples
        t = samples / freq  #time
        signal = np.frombuffer(song.readframes(samples), dtype=np.int16) #signal
        song.close() 
        print(f"Audio file loaded successfully: {samples} samples, {freq} Hz, {t:.2f} seconds.")
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return None

    print("Starting downsampling...")
    max_points = 2000 #lower resolution to compute faster
    step = max(1, len(signal) // max_points)
    signal = signal[::step]  #Reduce the number of samples
    samples = len(signal) #new number of samples w audio steps
    print(f"Downsampling complete: {samples} samples, original duration: {t:.2f} seconds.")

    #slider steps
    print("Generating traces and slider steps...")
    traces = []
    sliders_steps = []
    resolution_levels = [0.1, 0.25, 0.5, 1.0, 2.0]  #5 slider levels
    default_res_index = 3
    for i,res in enumerate(resolution_levels):  # Sample rates from 1 to 5
        print(f"Generating trace for sample rate {res}...")
        resampled_signal = resample(signal, int(samples * res))
        resampled_samples = len(resampled_signal)
        
        #x axis
        time_axis = np.linspace(0, t, num=resampled_samples)

        #Create traces to plot graph
        traces.append(
            go.Scatter(
                x=time_axis,
                y=resampled_signal,
                visible=(i == default_res_index),  # Show only the first trace initially
                name=f"Rate {res:.2f}",
            )
        )

        #slider step
        sliders_steps.append({
            "args": [{"visible": [j == i for j in range(len(resolution_levels))]}],
            "label": f"{res:.2f}",
            "method": "update",
        })

        print(f"Trace for resolution {res} generated with {resampled_samples} samples.")

    print("Traces and slider steps generated.")

    #make a layout
    print("Creating layout with slider...")
    layout = go.Layout(
        title="Waveform with scale slider",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
        sliders=[{
            "active": default_res_index,
            "currentvalue": {"prefix": "Graph scale: "},
            "steps": sliders_steps,
        }]
    )

    #make figure and json
    print("Generating final figure...")
    fig = go.Figure(data=traces, layout=layout)
    fig_json = json.loads(fig.to_json())
    print("Waveform generation complete. JSON output below:")
    print(json.dumps(fig_json, indent=2))  # Print the JSON for debugging

    return fig_json
