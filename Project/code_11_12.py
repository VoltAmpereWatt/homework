import cv2
import numpy as np
#Camera 0 is the integrated web cam on the laptop
camera_port = 0
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)
 
# Captures a single image from the camera and returns it in PIL format
def get_image():
 # read is the easiest way to get a full image out of a VideoCapture object.
 retval, im = camera.read()
 return im
x = get_image()
x = cv2.cvtColor(x, cv2.COLOR_RGB2GRAY)
avg_variable = np.zeros(np.shape(x),np.int8)
# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
for i in range(ramp_frames):
    temp = get_image()
    print("Taking image...")
# Take the actual image we want to keep
    camera_capture = get_image()
    camera_capture = np.int8(np.divide(cv2.cvtColor(camera_capture, cv2.COLOR_RGB2GRAY), ramp_frames))
    avg_variable += camera_capture
    print(avg_variable)
    file = "C:/Users/samad/OneDrive/Desktop/rsg/test_image_%d.png" %i

if input() == 'c':
    hand = get_image()
    hand = np.int8(cv2.cvtColor(hand, cv2.COLOR_RGB2GRAY))
    s = np.int8(np.subtract(avg_variable, hand))
    cv2.imwrite('subimage.png', s)
# avg_variable = avg_variable
# A nice feature of the imwrite method is that it will automatically choose the
# correct format based on the file extension you provide. Convenient!
cv2.imwrite(file, avg_variable)

# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
del(camera)

