import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = gray.copy()
    cv2.putText(gray, 'Put fingers across arc', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2)
    cv2.ellipse(gray, (320,240),(150,50), 0.0, 180.0, 360.0, (255,0,0),5)
    # Display the resulting frame
    cv2.imshow('frame',gray)
    if not ret:
        break
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "C:/Users/FITL Staff/Desktop/study-stuff/blah.png"
        cv2.putText(gray2, "Image Captured", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0),5) 
        cv2.ellipse(gray2, (320,240),(150,50), 0.0, 180.0, 360.0, (255,0,0),5)
        cv2.imwrite(img_name, gray2)
        

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()