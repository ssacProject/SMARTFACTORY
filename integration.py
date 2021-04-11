#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32

rospy.init_node('topic_pulisher')

pub = rospy.Publisher('counter', Int32)

rate = rospy.Rate(2)

# SDA = pin.SDA_1
# SCL = pin.SCL_1
# SDA_1 = pin.SDA
# SCL_1 = pin.SCL



from adafruit_servokit import ServoKit
import board
import busio
#from approxeng.input.selectbinder import ControllerResource

import time

import robotarm_mapping as robot
import cap_v_2 as capture
import dcmotor

for i in range(2):
    x, y=capture.cam_main()
    robot.servo(x, y, i)
    for j in range(5):
        pub.publish(j)    



