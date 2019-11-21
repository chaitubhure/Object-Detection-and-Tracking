'''
ECGR 5101 FINAL PROJECT
12/12/2018
REFERENCES:https://github.com/Mjrova
PROJECT TITLE: EYE MECHANISM FOR INMOOV ROBOT
PROJECT DESCRIPTION:
        picam is used for the video and it is being sampled frame by frame. We identify the contour of the object in the frame using
        opencv libraries and functionalities. With the help of contour we got the co-ordinates of the center point of the contour. As the object moves
        so does the contour and the co-ordinates. With the help of co-ordinates we give the output to the servo motor.


'''

# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import RPi.GPIO as GPIO

#define Servos GPIOs
panServo = 27
tiltServo = 17


#servo position
def posi_servo (servo, angle):
    os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
    print(" servo at GPIO {0} to {1} \n".format(servo, angle))

# position servos to present object at center of the snap
def servo_mapping (x, y):
    global panDegree
    global tiltDegree
    if (x < 220):
        panDegree += 10
        if panDegree > 150:
            panDegree = 150
        posi_servo (panServo, panDegree)

    if (x > 280):
        panDegree -= 10
        if panDegree < 80:
            panDegree = 80
        posi_servo (panServo, panDegree)

    if (y < 160):
        tiltDegree += 5
        if tiltDegree > 110:
            tiltDegree = 110
        posi_servo (tiltServo, tiltDegree)

    if (y > 210):
        tiltDegree -= 5
        if tiltDegree < 90:
            tiltDegree = 90
        posi_servo (tiltServo, tiltDegree)

# initialize  camera sensor to warmup
print(" camera to warmup...")
video = VideoStream(0).start()
time.sleep(2.0)

# define the lower and upper boundaries of object
colorLower = (24, 100, 100)
colorUpper = (44, 255, 255)


# Initialize angle servos at 110-105 position
global panDegree
panDegree = 110
global tiltDegree
tiltDegree =105

# positioning servos at initial position
posi_servo (panServo, panDegree)
posi_servo (tiltServo, tiltDegree)

# loop over the snaps from the video stream
while True:
    # next snap from the video stream
    #convert it to the HSV color space
    snap = video.read()
    snap = imutils.resize(snap, width=500)
    snap = imutils.rotate(snap, angle=180)
    hsv = cv2.cvtColor(snap, cv2.COLOR_BGR2HSV)

    # construct  mask for object color

    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # initialize the current (x, y) center of the object
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask

        c = max(cnts, key=cv2.contourArea)
        ((x, y), rad) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # proceed if the rad meets a minimum size
        if rad > 10:
            # draw the circle and centroid on snap
            cv2.circle(snap, (int(x), int(y)), int(rad),
                (0, 255, 255), 2)
            cv2.circle(snap, center, 5, (0, 0, 255), -1)

            # Servo at center
            servo_mapping(int(x), int(y))



    # show the snap to our screen
    cv2.imshow("snap", snap)

    # if [ESC] key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
            break

# do cleanup
print("\n  cleanup stuff \n")
GPIO.cleanup()
cv2.destroyAllWindows()
video.stop()
