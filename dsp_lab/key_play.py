# key_play.py

"""
PyAudio Example: Generate random pulses and input them to an IIR filter of 2nd order.
Original version by Gerald Schuller, March 2015 
Modified by Ivan Selesnick, October 2015
"""

import pyaudio
import struct
import numpy as np
from math import sin, cos, pi
import cv2

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 2         # Mono
RATE        = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 1      # Decay time (seconds)
f1 = 1600    # Frequency (Hz)
Tb = 5
f2 = 400
# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om1 = 2.0 * pi * float(f1)/RATE

# Filter coefficients (second-order IIR)
a1 = -2*r*cos(om1)
a2 = r**2
b0 = sin(om1)
a3 = -2*r*sin(om1)
a4 = r**3
b1 = cos(om1)
# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
        format      = PA_FORMAT,
        channels    = CHANNELS,
        rate        = RATE,
        input       = False,
        output      = True,
        frames_per_buffer = 256)
# specify low frames_per_buffer to reduce latency


print('Select the image window, then press keys for sound.')
print('Press "q" to quit')

y = np.zeros(BLOCKLEN)
y2 = np.zeros(BLOCKLEN)
x = np.zeros(BLOCKLEN)

img = cv2.imread('NotPossibleCases.png')
cv2.imshow('image', img)

while True:

    key = cv2.waitKey(1)

    if key == -1:
        # No key was pressed
        x[0] = 0.0        
    elif key == ord('q'):
        # Quit if user presses 'q'
        break
    elif key == ord('a'):
        # Some key (other than 'q') was pressed
        x[0] = 15000.0 
    elif key == ord('d'):
        x[0] = 5000.0 

    # Run difference equation for block
    for n in range(BLOCKLEN):
        y[n] = b0 * x[n] - a1 * y[n-1] - a2 * y[n-2] 
        y2[n] = b1 * x[n] - a3 * y[n-1] - a4 * y[n-2]

        # What happens when n = 0?
        # In Python, negative indices cycle to end, which is appropriate here

    y = np.clip(y.astype(int), -MAXVALUE, MAXVALUE)     # Clipping

    y2 = np.clip(y2.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    # Convert numeric list to binary string
    data = struct.pack('h' * BLOCKLEN, *y)
    data += struct.pack('h' * BLOCKLEN, *y2)
    # Write binary string to audio output stream
    stream.write(data, BLOCKLEN)

print('* Done *')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()

