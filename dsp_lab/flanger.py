import pyaudio
import wave
import struct
import math
import numpy 
from myfunctions import clip16
# wavfile = 'sin01_mono.wav'
wavfile = 'author.wav'
outfile = 'flanger.wav'

print('Now playing',outfile)

wf = wave.open( wavfile, 'rb')
wf2 = wave.open( outfile, 'wb')

# Read wave file properties
RATE        = wf.getframerate()     # Frame rate (frames/second)
WIDTH       = wf.getsampwidth()     # Number of bytes per sample
LEN         = wf.getnframes()       # Signal length
CHANNELS    = wf.getnchannels()     # Number of channels

wf2.setframerate(RATE)
wf2.setsampwidth(WIDTH)
wf2.setnframes(LEN)
wf2.setnchannels(CHANNELS)

# print('The file has %d channel(s).'         % CHANNELS)
# print('The file has %d frames/second.'      % RATE)
# print('The file has %d frames.'             % LEN)
# print('The file has %d bytes per sample.'   % WIDTH)
out = bytes([])
BUFFER_LEN =  200                          # Buffer length
buffer = [0.0 for i in range(BUFFER_LEN)]   # Initialize to zero

p = pyaudio.PyAudio()
stream = p.open(
    format      = pyaudio.paInt16,
    channels    = 1,
    rate        = RATE,
    input       = False,
    output      = True )

delayPattern = list(numpy.linspace(0,2*math.pi,LEN))
delayPattern = list(numpy.ceil(100*numpy.cos(delayPattern)))
for a in range(0,len(delayPattern)):
    delayPattern[a] = int(delayPattern[a]+99)

b0,b1 = (1,0.954321)
x0 = 0
for n in range(0,LEN):
    input_string = wf.readframes(1)

    # Convert string to number
    input_value = struct.unpack('h', input_string)[0]
    x0 = input_value

    output_value = b0*x0 + b1*buffer[delayPattern[n]-1]
    buffer[n%BUFFER_LEN]=output_value

    
    output_string = struct.pack('h', int(clip16(output_value)))

    # Write output to audio stream
    stream.write(output_string)
    out += output_string 
    # wf2.writeframes(output_string)
    # output_all = output_all + output_string     # append new to total

print('* Finished *')

stream.stop_stream()
stream.close()
p.terminate()
wf.close()
wf2.writeframes(out)
wf2.close()