import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
cv2.namedWindow('Trackbar window')

#Open webcam, choose the nbr change '0' to nbr of your webcam
capture = cv2.VideoCapture(0)

# create trackbars for color change
cv2.createTrackbar('H_high','Trackbar window',0,179,nothing)
cv2.createTrackbar('S_high','Trackbar window',0,255,nothing)
cv2.createTrackbar('V_high','Trackbar window',0,255,nothing)
cv2.createTrackbar('H_low','Trackbar window',0,179,nothing)
cv2.createTrackbar('S_low','Trackbar window',0,255,nothing)
cv2.createTrackbar('V_low','Trackbar window',0,255,nothing)
cv2.createTrackbar('high','Trackbar window',0,255,nothing)
cv2.createTrackbar('low','Trackbar window',0,255,nothing)


#Setting the "high" trackbars to max values (255)
cv2.setTrackbarPos('H_high','Trackbar window', 179)
cv2.setTrackbarPos('S_high','Trackbar window', 255)
cv2.setTrackbarPos('V_high','Trackbar window', 255)
cv2.setTrackbarPos('high','Trackbar window', 255)
cv2.setTrackbarPos('low','Trackbar window', 0)


while(1):
    _, frame = capture.read()
    cv2.imshow('Trackbar window', np.zeros((1,512,4), np.uint8))
    img = frame
    
    _f = cv2.medianBlur(frame, 15)
    _f = cv2.cvtColor(_f, cv2.COLOR_BGR2HSV) #To HSV

    # get current positions of four trackbars 
    #These are HSV values
    h_low = cv2.getTrackbarPos('H_low','Trackbar window')
    s_low = cv2.getTrackbarPos('S_low','Trackbar window')
    v_low = cv2.getTrackbarPos('V_low','Trackbar window')
    h_high = cv2.getTrackbarPos('H_high','Trackbar window')
    s_high = cv2.getTrackbarPos('S_high','Trackbar window')
    v_high = cv2.getTrackbarPos('V_high','Trackbar window')
    low = cv2.getTrackbarPos('low','Trackbar window')
    high = cv2.getTrackbarPos('high','Trackbar window')

    # define range of color in HSV
    lower_bound = np.array([h_low,s_low,v_low])
    upper_bound = np.array([h_high,s_high,v_high])
    
    
    mask = cv2.inRange(_f, lower_bound, upper_bound)
    frame = cv2.bitwise_and(frame, frame, mask = mask) #Comment this line if you won't show the frame later

    #Comment the one you won't need
    cv2.imshow('HSV',_f)
    cv2.imshow('img',img)
    #cv2.imshow('mask',mask)
    
    
    image = frame
    # Gaussian blur
    Gblur = cv2.GaussianBlur(mask,(5,5),0)
    ret,thresh1 = cv2.threshold(Gblur,low,high,cv2.THRESH_BINARY_INV)
    mask2 = cv2.erode(thresh1, None, iterations=2)
    mask2 = cv2.dilate(mask2, None, iterations=2)
    mask2 = cv2.bitwise_not(mask2)
    contours,hierarchy = cv2.findContours(mask2.copy(), 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        cv2.line(image,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(image,(0,cy),(1280,cy),(255,0,0),1)

        cv2.drawContours(image, contours, -1, (0,255,0), 1)
    cv2.imshow('image',image)
    cv2.imshow('mask2',mask2)


    k = cv2.waitKey(1) & 0xFF
    if k == 27: #press escape to exit
        break

    
capture.release()   #Release the camera
cv2.destroyAllWindows() #Close all windows