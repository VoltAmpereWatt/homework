import struct
import pyaudio
import wave
import numpy  as np
from myfunctions import clip16
import math

def zeros(n):
    return [0]*n

sampFreq=8000
K = 0.99
T = 3.0
N = 80
gain = 7000
samples = N + int(T*sampFreq)

# Declaring Input Signal
x = zeros(N+int(T*sampFreq))

for i in range(len(x)):
	if i<=N-1:
		x[i] = np.random.randn(1)[0]
	else:
		x[i] = 0.0


# Difference equation

p = pyaudio.PyAudio()
stream = p.open(
	format= pyaudio.paInt16,
	channels = 1,
	rate  = sampFreq,
	input = False,
	output= True )

# N delays required, so buffer of length N.

buffer = zeros(N)
k = 0
G = 1000

for n in range(samples):
	input_value=x[n]
	# Circular buffer implementation for when end of buffer reached
	if k==N-1:
		yN=buffer[0]
	else:
		yN=buffer[k+1]
		
	yN1=buffer[k]
	# Implementing difference equation
	output_value = input_value + (K/2) *(yN + yN1)
	# Update buffer 
	buffer[k] = output_value
	k = k + 1
	if k > N-1:
		k = 0
	
    # Writing to audio output, limiting to 16 bit values.
	output_string = struct.pack('h', int(clip16(output_value*G)))

	# Write output to audio stream
	stream.write(output_string)

print('* Finished')