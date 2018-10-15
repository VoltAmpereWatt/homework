# play_vibrato_ver2.py
# Reads a specified wave file (mono) and plays it with a vibrato effect.
# (Sinusoidal time-varying delay)
# This implementation uses a circular buffer with two buffer indices.
# Uses linear interpolation

import pyaudio
import wave
import struct
import math
from myfunctions import clip16

# # TRY BOTH WAVE FILES
# wavfile = 'sin01_mono.wav'
# wavfile = 'decay_cosine_mono.wav'

# Open wave file

# Read wave file pr

# Vibrato parameters
f0 = 2
W = 0.2
# W = 0 # for no effct

# f0 = 10
# W = 0.2

# OR
# f0 = 20
# ratio = 1.06
# W = (ratio - 1.0) / (2 * math.pi * f0 )
# print W

# Create a buffer (delay line) for past values
buffer_MAX =  64                          # Buffer length
buffer = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

output_value = [0.0 for i in range(buffer_MAX)]   # Initialize to zero
# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
kw = buffer_MAX/2

# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print('The buffer is {0:d} samples long.'.format(buffer_MAX))

WIDTH = 2
CHANNELS = 1 
RATE = 16000
DURATION = 5
# Open an output audio stream
p = pyaudio.PyAudio()

stream = p.open(format      = pyaudio.get_format_from_width(WIDTH),
                channels    = CHANNELS,
                rate        = RATE,
                input       = True,
                output      = True )


# output_all = ''            # output signal in all (string)
output_all = bytes([])            # output signal in all (string)

print ('* Playing...')
output_buffer = []
Nblocks = math.ceil(DURATION*RATE/buffer_MAX)


input_string = stream.read(buffer_MAX, exception_on_overflow = False)
# Loop through wave file 
for n in range(Nblocks):

    # Get sample from wave file

    input_value = struct.unpack('h'*buffer_MAX, input_string)
    # print('Length of input_value list: ',len(input_value))


    #    input_string = wf.readframes(buffer_MAX)
    # print(len(input_value))
    # Convert string to number
    # print('Length of output_value list: ',len(output_value))

    for z in range(len(input_value)):
 
        # Get previous and next buffer values (since kr is fractional)
        kr_prev = int(math.floor(kr))               
        kr_next = kr_prev + 1
        frac = kr - kr_prev    # 0 <= frac < 1
        if kr_next >= buffer_MAX:
            kr_next = kr_next - buffer_MAX

        # Compute output value using interpolation
        output_value[z] = (1-frac) * buffer[kr_prev] + frac * buffer[kr_next]
        output_value[z] = int(clip16(output_value[z]))
        # Update buffer (pure delay)
        buffer[int(kw)] = input_value[z]

        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * z / RATE )
            # Note: kr is fractional (not integer!)

        # Ensure that 0 <= kr < buffer_MAX
        if kr >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr = 0

        # Increment write index    
        kw = kw + 1
        if kw == buffer_MAX:
            # End of buffer. Circle back to front.
            kw = 0
        # output_value.append()
    # Clip and convert output value to binary string

    output_string = struct.pack('h'*buffer_MAX, *output_value)
    # Write output to audio stream
    stream.write(output_string)

    output_all = output_all + output_string     # append new to total
    input_string = stream.read(buffer_MAX, exception_on_overflow = False)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
