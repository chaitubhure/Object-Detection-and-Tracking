ECGR_5101_Project
----------------EYE MECHANISM FOR InMooV ROBOT------------------
Pre-req : Raspberry Pi OS (Rasbian), OpenCV, Memory Card.

NOTE:
Use "pi" as the id and "raspberry" as the password.

RaspberryPi Setup:
1) Connect Pi to the supply.
2) Connect the LAN cable to the Laptop/Desktop via Router.
3) Set up Wireless connection for the Pi using PuTTy.
4) Set up TightVNC Viewver to use your Laptop/Desktop as a display for the Pi.

Servo Motor Connection:
1) Connect the Pan Servo Motor to GPIO 27.
2) Connect the Tilt Servo to the GPIO 17.
3) Connect the power supply to the servos.

Code Compile:
1) Check if OpenCV is installed properly
   -- cv2.__version__
2) Check if the system variables have been setup correctly
   -- source ~/.profile
3) Enter the virtual Environment
   -- workon cv
4) Enter the python code directory
   -- cd OpenCV_Object_Track/Object_Tracking
5) Check if PiCam is set up properly
   -- raspistill -o <imagename.jpg>
5) Check for camera dependencies
   -- sudo modprobe bcm2835-v4l2
6) Run the .py file for image tracking and servo motor control
   -- python objectDetecTrack.py