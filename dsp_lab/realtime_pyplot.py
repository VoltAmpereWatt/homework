from matplotlib import pyplot 
from myfunctions import clip16
from scipy.signal import butter, lfilter

import pyaudio
import wave
import struct
import math

wavefile = 'sin01_mono.wav'
outfile  = 'sin01_mono_filtered.wav'

print('Play the wave file %s.' % wavefile)

wf = wave.open(wavefile, 'rb')
wf2 = wave.open(outfile, 'wb')

num_channels    = wf.getnchannels()     # Number of channels
RATE            = wf.getframerate()     # Sampling rate (frames/second)
signal_length   = wf.getnframes()       # Signal length
width           = wf.getsampwidth()     # Number of bytes per sample

wf2.setnchannels(num_channels)
wf2.setnframes(signal_length)
wf2.setsampwidth(width)
wf2.setframerate(RATE)

print('The file has %d channel(s).'            % num_channels)
print('The frame rate is %d frames/second.'    % RATE)
print('The file has %d frames.'                % signal_length)
print('There are %d bytes per sample.'         % width)

#Filter constants

(b,a) = butter(1,[0.4,0.8],btype='pass')
(b0,b1,b2) = b
(a1,a2,a3) = a

#Initial States
(x1,x2,x3,x4) = (0.0,0.0,0.0,0.0)
(y1,y2,y3,y4) = (0.0,0.0,0.0,0.0)

p = pyaudio.PyAudio()

stream = p.open(
    format      = pyaudio.paInt16,
    channels    = num_channels,
    rate        = RATE,
    input       = False,
    output      = True )

input_string = wf.readframes(1)

val = struct.unpack('h', input_string)

fig = pyplot.figure()
pyplot.ion()
line, = pyplot.plot(val)

bufflen = 200

pyplot.ylim(-32000, 32000)
pyplot.xlim(0, bufflen)
var = 1
ip,op = ([],[])
pyplot.show
while len(input_string) > 0:
    input_tuple = struct.unpack('h', input_string)  # One-element tuple
    input_value = input_tuple[0]

    x0 = input_value
    ip.append(x0)
    y0 = x0 + b1*x1 + b2*x2 - a1*y1 - a2*y2 - a3*y3 
    
    (y3,y2,y1) = (y2,y1,y0)
    (x3,x2,x1) = (x2,x1,x0)
    
    output_value = int(clip16(y0))
    op.append(output_value)
    
    if var == bufflen-1:
#         pyplot.setp(line,ydata=op)
        pyplot.plot(op,'b')
        pyplot.plot(ip,'r')
#         pyplot.show()
        # pyplot.draw()
        pyplot.pause(0.001)
#         pyplot.draw()
        (var,op,ip) = (0,[],[])
        # pyplot.pause(0.001)
        pyplot.cla()
    # pyplot.show()        
    var+=1
    output_string = struct.pack('h', output_value)
    stream.write(output_string)
    wf2.writeframes(output_string)
    
    input_string = wf.readframes(1)


wf.close()
wf2.close()
stream.stop_stream()
stream.close()
p.terminate()
