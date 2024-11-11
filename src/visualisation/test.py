import wave as wv   #To open wav files
import numpy as np  #To analyse audio bits
import matplotlib.pyplot as plt #To plot a frequency graph

song = wv.open('./src/test_mp3s/thx.wav', 'rb')
freq = song.getframerate() #Get the frequency of the audio
samples = song.getnframes() #n samples
t = samples / freq #time
nchannels = song.getnchannels()
print(f"Frequency: {freq} Hz", f"Samples: {samples}", f"Time: {t} seconds", f"Number channels: {nchannels}", sep='\n')

signal = song.readframes(samples)