import pyaudio
import struct
import wave
import math
from matplotlib import pyplot,animation 
import numpy as np
from scipy import signal

def buncher(var,x):
    var += x
    return var 

ipfull = []
opfull = []
blocklen = 64

wavfile = 'block_n_filter.wav'

# print('Play the wave file %s.' % wavfile)

# Open wave file (should be mono channel)
wf = wave.open( wavfile, 'wb' )

# Read the wave file properties
channels          = 1     # Number of channels
rate              = 16000     # Sampling rate (frames/second)
signal_duration   = 5       # Signal length
signal_length     = rate*signal_duration 
width             = 2     # Number of bytes per sample
MAXVALUE = 2**15 - 1
print('The file has %d channel(s).'            % channels)
print('The frame rate is %d frames/second.'    % rate)
print('The file has %d frames.'                % signal_length)
print('There are %d bytes per sample.'         % width)

wf.setnchannels(channels)
wf.setsampwidth(width)
wf.setframerate(rate)

p = pyaudio.PyAudio()
stream = p.open(
    format      = p.get_format_from_width(width),
    channels    = 1,
    rate        = rate,
    input       = True,
    output      = True)

# Create block (initialize to zero)
output_block = [0 for n in range(0, blocklen)]

# Difference equation coefficients
b0 =  0.008442692929081
b2 = -0.016885385858161
b4 =  0.008442692929081
b = [b0, 0.0, b2, 0.0, b4]

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 =  4.942669993770672
a3 = -3.114402101627517
a4 =  0.757546944478829
a = [1.0, a1, a2, a3, a4]

binary_data = stream.read(blocklen,exception_on_overflow = False)
input_block = struct.unpack('h' * blocklen, binary_data)
# input_block = np.array(input_block)

numblocks = math.ceil(signal_length/blocklen)
ORDER = 4   # filter is fourth order
states = np.zeros(ORDER)
var = 1

# pyplot.ion()
# fig = pyplot.figure(1)

for x in range(numblocks):

    input_block = struct.unpack('h' * blocklen, binary_data) 
    output_block, states = signal.lfilter(b, a, input_block, zi = states)
    # clipping
    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)     
    # convert to integer
    output_block = output_block.astype(int)        
    #converting to format suited for output to device
    binary_data = struct.pack('h' * blocklen, *output_block)  
    pyplot.plot(input_block,'r',label='Input Block')
    pyplot.plot(output_block,'g',label='Output Block')
    pyplot.axis([0,65,-10000,10000])
    pyplot.grid()
    pyplot.legend(loc = 'upper right')
    pyplot.draw()
    pyplot.pause(0.001)
    pyplot.cla()
    # Write binary data to audio stream
    stream.write(binary_data)                     

    # Write binary data to output wave file
    wf.writeframes(binary_data)
    
    # Get next frame from wave file
    binary_data = stream.read(blocklen,exception_on_overflow = False)

print('* Finished')
pyplot.close()
stream.stop_stream()
stream.close()
p.terminate()
wf.close()

