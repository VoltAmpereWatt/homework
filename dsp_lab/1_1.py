# plot_microphone_input_spectrum.py

"""
Using Pyaudio, get audio input and plot real-time FFT of blocks.
Ivan Selesnick, October 2015
Based on program by Gerald Schuller
"""

import pyaudio
import math
import struct
from matplotlib import pyplot as plt
import numpy as np

plt.ion()           # Turn on interactive mode so plot gets updated
f0 = 400    # 'Duck' audio
WIDTH     = 2         # bytes per sample
CHANNELS  = 1         # mono
RATE      = 8000     # Sampling rate (samples/second)
BLOCKSIZE = 1024      # length of block (samples)
DURATION  = 10        # Duration (seconds)

NumBlocks = int( DURATION * RATE / BLOCKSIZE )

print('BLOCKSIZE =', BLOCKSIZE)
print('NumBlocks =', NumBlocks)
print('Running for ', DURATION, 'seconds...')

# DBscale = False
DBscale = True

# Initialize plot window:
plt.figure(1)
if DBscale:
    plt.ylim(0, 150)
else:
    plt.ylim(0, 20*RATE)

# Initialize phase
om = 2*math.pi*f0/RATE
theta = 0

# Frequency axis (Hz)
plt.xlim(0, 0.5*RATE)         # set x-axis limits
# plt.xlim(0, 2000)         # set x-axis limits
plt.xlabel('Frequency (Hz)')
f = RATE/BLOCKSIZE * np.arange(0, BLOCKSIZE)

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(f)                         # x-data of plot (frequency)

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)

stream = p.open(
    format    = PA_FORMAT,
    channels  = CHANNELS,
    rate      = RATE,
    input     = True,
    output    = True)

output_block = [0 for n in range(0, BLOCKSIZE)]

for i in range(0, NumBlocks):
    input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
    # print(input_string)
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert
    # print(input_tuple)
    X = np.fft.fft(input_tuple)

    for n in range(0, BLOCKSIZE):
        # Amplitude modulation  (f0 Hz cosine)
        theta = theta + om
        output_block[n] = int( input_tuple[n] * math.cos(theta) )
        # output_block[n] = input_tuple[n]  # for no processing

    # keep theta betwen -pi and pi
    while theta > math.pi:
        theta = theta - 2*math.pi


    # Update y-data of plot
    if DBscale:
        line.set_ydata(20*np.log10(abs(X)))
    else:
        line.set_ydata(abs(X))
    plt.pause(0.001)
    plt.draw()
    
    binary_data = struct.pack('h' * BLOCKSIZE, *output_block)

    # Write binary data to audio output stream
    stream.write(binary_data)


plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print('* Finished')
