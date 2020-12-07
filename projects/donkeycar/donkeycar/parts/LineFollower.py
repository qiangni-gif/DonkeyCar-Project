#!/usr/bin/env python3
"""

Usage:
    manage.py --name=your_name


Options:
    -h --help          Show this screen.    
"""
import os
import time

from docopt import docopt
import numpy as np
import cv2

import donkeycar as dk
from donkeycar.parts.datastore import TubHandler
import time


class LineFollower:
    '''
    OpenCV based controller
    This controller takes a horizontal slice of the image at a set Y coordinate.
    Then it converts to HSV and does a color thresh hold to find the yellow pixels.
    It does a histogram to find the pixel of maximum yellow. Then is uses that iPxel
    to guid a PID controller which seeks to maintain the max yellow at the same point
    in the image.
    '''
    def __init__(self):
        self.scan_y = 60   # num pixels from the top to start horiz scan
        self.scan_height = 10 # num pixels high to grab from horiz scan
        # self.color_thr_low = np.asarray((0, 50, 50)) # hsv dark yellow
        # self.color_thr_hi = np.asarray((50, 255, 255)) # hsv light yellow
        self.color_thr_low = np.array([70, 15, 0]) # black
        self.color_thr_hi = np.array([130, 100, 70]) # black
        #self.color_white_low = np.asarray((25, 10, 32)) # white low
        #self.color_white_hi = np.asarray((110, 60, 100)) # white hi
        self.color_green_low = np.array([82, 200, 50]) # green low
        self.color_green_hi = np.array([120, 255, 130]) # green hi

        self.steering = 0.0 # from -1 to 1
        self.throttle = 0.0 # from -1 to 1
        self.recording = False # Set to true if desired to save camera frames
        self.delta_th = 0.05 # how much to change throttle when off
        self.throttle_max = 0.5
        self.throttle_min = 1
        
        self.linefollower_setting = False

    
    def get_i_color(self, cam_img, low, hi):

        '''
        get the horizontal index of the color at the given slice of the image
        input: cam_image, an RGB numpy array
        output: index of max color, value of cumulative color at that index, and mask of pixels in range 
        '''

        # take a horizontal slice of the image
        iSlice = self.scan_y
        #print(type(cam_img))
        scan_line = crop_img[iSlice : iSlice + self.scan_height, :, :]
        

        # convert to HSV color space
        img_hsv = cv2.cvtColor(scan_line, cv2.COLOR_RGB2HSV)

        # make a mask of the colors in our range we are looking for
        mask = cv2.inRange(img_hsv, low, hi)

        # which index of the range has the highest amount of this color?
        hist = np.sum(mask, axis=0)
        max_color = np.argmax(hist)

        return max_color, hist[max_color], mask
    
    def nothing(self,x):
        pass
    def get_hsv(self, crop_img, low, hi):
        # cv2.namedWindow('Trackbar window')

        # cv2.createTrackbar('H_high','Trackbar window',0,179,self.nothing)
        # cv2.createTrackbar('S_high','Trackbar window',0,255,self.nothing)
        # cv2.createTrackbar('V_high','Trackbar window',0,255,self.nothing)
        # cv2.createTrackbar('H_low','Trackbar window',0,179,self.nothing)
        # cv2.createTrackbar('S_low','Trackbar window',0,255,self.nothing)
        # cv2.createTrackbar('V_low','Trackbar window',0,255,self.nothing)


        # cv2.setTrackbarPos('H_high','Trackbar window', 179)
        # cv2.setTrackbarPos('S_high','Trackbar window', 255)
        # cv2.setTrackbarPos('V_high','Trackbar window', 255)
        # while(1):
        #     cv2.imshow('Trackbar window', np.zeros((1,512,4), np.uint8))
        #     h_low = cv2.getTrackbarPos('H_low','Trackbar window')
        #     s_low = cv2.getTrackbarPos('S_low','Trackbar window')
        #     v_low = cv2.getTrackbarPos('V_low','Trackbar window')
        #     h_high = cv2.getTrackbarPos('H_high','Trackbar window')
        #     s_high = cv2.getTrackbarPos('S_high','Trackbar window')
        #     v_high = cv2.getTrackbarPos('V_high','Trackbar window')

            # low = np.array([h_low,s_low,v_low])
            # hi = np.array([h_high,s_high,v_high])

        img_hsv = cv2.medianBlur(crop_img, 15)
        img_hsv = cv2.cvtColor(img_hsv, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(img_hsv, low, hi)
        blur = cv2.GaussianBlur(mask,(5,5),0)
        ret,thresh1 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV)
        mask2 = cv2.erode(thresh1, None, iterations=2)
        mask2 = cv2.dilate(mask2, None, iterations=2)
        mask2 = cv2.bitwise_not(mask2)

            # cv2.imshow("hsc",mask2)
            # cv2.imshow("crop",crop_img)
            # k = cv2.waitKey(1) & 0xFF
            # if k == 27: #press escape to exit
            #     break
        
        return mask2

    
 
    def detect_color(self,mask):
        fcolor = False
        hasGreen = np.sum(mask)# number of white pixel
        if hasGreen > 150000:
            fcolor = True
            print("color detected:", hasGreen )
        else:
            fcolor = False
        return fcolor

    def find_contours(self,crop_img,img, mask):
        contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
            return cx
        return None
    


    def run(self, cam_img, mode, linefollower_setting):
        '''
        main runloop of the CV controller
        input: cam_image, an RGB numpy array
        output: steering, throttle, and recording flag
        '''
        if cam_img is not None:
            detect = False
            self.linefollower_setting = linefollower_setting
            # max_color, confidense, mask = self.get_i_color(cam_img, self.color_green_low, self.color_green_hi)
            crop_img = cam_img[40:120, 0:160]
            Gmask = self.get_hsv(crop_img, self.color_green_low, self.color_green_hi)
            Bmask = self.get_hsv(crop_img, self.color_thr_low, self.color_thr_hi)
            detect = self.detect_color(Gmask)
            
            if self.linefollower_setting == True and detect == True :
                CX = self.find_contours(crop_img,cam_img, Gmask)
            else:
                CX = self.find_contours(crop_img,cam_img, Bmask)
            cv2.imshow("Bmask",Bmask)
            cv2.imshow("Gmask",Gmask)

            cv2.imshow("img",cam_img)
            cv2.waitKey(1) 
               
            print(CX)
            if mode == 'LineFollower': #4900
            # print("LineFollower: mode is LineFollower")
                if CX == None:
                    self.throttle = 0.0
                    self.steering = 0.0
                elif CX >= 140:
                    self.steering = 1.0
                    self.throttle = self.throttle_min
                    print("turing right")

                elif CX < 140 and CX > 70:
                    self.steering = 0.0
                    self.throttle = self.throttle_max
                    print("forward")

                elif CX <= 70:
                    self.steering = -1.0
                    self.throttle = self.throttle_min
                    print("turing left")
                else:
                    self.throttle = 0.0
                    self.steering = 0.0

        else: #linefollow is set to off
            self.throttle = 0.0
            self.steering = 0.0
                
            # show some diagnostics
            #self.debug_display(cam_img, mask, max_color, confidense)
        print("steering:", self.steering,"  throttle:", self.throttle)

        return self.steering, self.throttle, self.recording
        
