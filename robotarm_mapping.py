# SDA = pin.SDA_1
# SCL = pin.SCL_1
# SDA_1 = pin.SDA
# SCL_1 = pin.SCL

from adafruit_servokit import ServoKit
from sympy import *
import board
import busio
import time
#from approxeng.input.selectbinder import ControllerResource


# On the Jetson Nano
# Bus 0 (pins 28,27) is board SCL_1, SDA_1 in the jetson board definition file
# Bus 1 (pins 5, 3) is board SCL, SDA in the jetson definition file
# Default is to Bus 1; We are using Bus 0, so we need to construct the busio first ...

print("Initializing Servos")
i2c_bus1=(busio.I2C(board.SCL, board.SDA))

print("Initializing ServoKit")
kit = ServoKit(channels=8)

# kit[0] is the bottom servo
# kit[1] is the top servo

print("Done initializing")

angle = [[0]*3 for _ in range(7)] 

theta1 = 0
theta3 = 0
theta4 = 0
belt_length = 5

def servo(x, y,count):
	print("x,y : ", x,y)
	servo_angle_min = 0  # Min pulse length out of 4096
	servo_angle_max = 180  # Max pulse length out of 4096
	
	#x,y mapping
	y_point = (310-x)/20
	x_point = (y-175)/20

	theta1_angle = atan(y_point/x_point)
	theta1 = round(theta1_angle,3)*6 + 160
	xpos = x_point/cos(theta1_angle)
	print("xpos",xpos)
    

	xpos_round=round(xpos,3)
	with open('output.csv','r') as file:
		csv_data = []
		for line in file.readlines():
			csv_data.append(line.replace('\n','').split(','))
		row_count = sum(1 for row in csv_data)
		for i in range(row_count-1): 
			if float(csv_data[i+1][2])<=xpos_round<=float(csv_data[i][2]): # x_distance
				theta3 = int(csv_data[i][0])
				theta4 = int(csv_data[i][1])

	print("theta1",theta1)
	print("theta3",theta3)
	print("theta4",theta4)

	#1st motor_path1
	angle[0][0] = 70 	        	#init_angle
	angle[0][1] = 0 			#goal_angle_1st

	#1st motor_path2
	angle[1][0] = theta1+4-xpos    		#break_angle_1st
	angle[1][1] = 70 			#goal_angle_1st_another

	#2nd motor
	angle[2][0] = 88+xpos	    	#init_angle_2nd
	angle[2][1] = 50 			#goal_angle_2nd
	angle[2][2] = 110 			#goal_angle_2nd


	#3rd motor
	angle[3][0] = 55 			#init_angle_3rd
	angle[3][1] = theta3 	        	#goal_angle_3rd
	angle[3][2] = 120

	#4th motor
	angle[4][0] = 55 		        #init_angle_4th
	angle[4][1] = theta4 			#goal_angle_4th

	#5th motor
	angle[5][0] = 90 			#init_angle_5th
	angle[5][1] = 36 			#goal_angle_5th

	#6th motor
	angle[6][0] = 40 			#init_angle_6th
	angle[6][1] = 0 			#goal_angle_6th

	step0 = 100
	step1 = 100
	step2 = 150
	step3 = 200


#if x == mapping[i][3], 

#mapping[i][3]==1/cos@*x => return [i][1], [i][2]
#motor6_angle = arctan(y/x)


	#-------Claws open_6th motor---------#
	kit.servo[3].angle=angle[3][0]
	kit.servo[2].angle=angle[2][1]


	#------1st motor & 3rd motor_init to goal--------#
	for sweep in range(step0):
	    kit.servo[1].angle=angle[0][0] + int(sweep*(angle[1][0]-angle[0][0])/step0)
	    kit.servo[3].angle=angle[3][1]-int(sweep*(angle[3][1]-angle[3][0])/step0)
	    time.sleep(0.01)

	#-------Claws open_6th motor---------#
	kit.servo[6].angle=angle[6][1]


	#------3rd motor & 2nd motor_init to goal--------#
	for sweep in range(step1):
	    kit.servo[3].angle=angle[3][0] + int(sweep*(angle[3][1]- angle[3][0])/step1)
	    kit.servo[2].angle=angle[2][1] + int(sweep*(angle[2][0] - angle[2][1])/step1)
	    kit.servo[4].angle=angle[4][0] + int(sweep*(angle[4][1] - angle[4][0])/step1)
	    time.sleep(0.01)
	time.sleep(0.5)

	#-------Claws close_6th motor---------#
	kit.servo[6].angle=angle[6][0]
	time.sleep(0.5)


	#------2nd motor_init to goal & 1st motor_break to goal--------#
	for sweep in range(step2):
	    kit.servo[2].angle=angle[2][0] - int(sweep*(angle[2][0] - angle[2][1])/step2)
	    kit.servo[4].angle=angle[4][1] + int(sweep*(angle[4][0] - angle[4][1])/step2)
	    if count == 0:
	        kit.servo[1].angle=angle[1][0] + int(sweep*(angle[1][1]- angle[1][0])/step2)
	    elif count == 1: 
	        kit.servo[1].angle=angle[1][0] + int(sweep*(angle[0][1]- angle[1][0])/step2)
	    time.sleep(0.01)


	#------3rd motor & 2nd motor_init to goal--------#
	for sweep in range(step2):
	    kit.servo[3].angle=angle[3][1] + int(sweep*(angle[3][2]-angle[3][1])/step2)
#	    kit.servo[2].angle=angle[2][1] + int(sweep*(angle[2][2] - angle[2][1])/step2)
	    if count == 0:
	        kit.servo[2].angle=angle[2][1] + int(sweep*(angle[2][2] - angle[2][1])/step2)
	    elif count == 1:
	        kit.servo[2].angle=angle[2][1] + int(sweep*(angle[2][0]- angle[2][1])/step2)

	    time.sleep(0.01)
	time.sleep(0.3)


	#-------Claws open_6th motor---------#
	kit.servo[6].angle= angle[6][1]
	time.sleep(0.5)

	#------3rd motor & 2nd motor_goal to init--------#
	for sweep in range(step2):
	    kit.servo[3].angle=angle[3][2] - int(sweep*(angle[3][2] -angle[3][0])/step2)
	    #kit.servo[2].angle=angle[2][2] - int(sweep*(angle[2][2] - angle[2][1])/step2)
	    time.sleep(0.015)
	    if count == 0:
	        kit.servo[1].angle=angle[1][1] - int(sweep*(angle[1][1]- angle[0][0])/step2)
	        kit.servo[2].angle=angle[2][2] - int(sweep*(angle[2][2]- angle[2][1])/step2)
	    if count == 1:
	        kit.servo[1].angle=angle[0][1] - int(sweep*(angle[0][1]- angle[0][0])/step2)
	        kit.servo[2].angle=angle[2][0] - int(sweep*(angle[2][0]- angle[2][1])/step2)
	time.sleep(0.5)


	#-------Claws close_6th motor---------#
	kit.servo[6].angle=angle[6][0]

'''
	#------1st motor_goal to init--------#
	for sweep in range(angle[0][1]-angle[0][0]):
	    kit.servo[1].angle=angle[0][1] - sweep
	    time.sleep(0.02)




	#5th motor

	#intial point
	kit.servo[5].angle=init_angle_5th
	time.sleep(1)

	#goal point
	kit.servo[5].angle=goal_angle_5th
	time.sleep(1)

	kit.servo[5].angle=init_angle_5th
	time.sleep(1)
	

	
	#default
	#------4th motor--------#
	kit.servo[4].angle=72

	#------4th motor--------#
	for sweep in range(55):
	    pwm.set_pwm(4, 0, servo_min + eighteen_degree*5 -j)
	    time.sleep(0.01)

	#goal point
	pwm.set_pwm(4, 0, servo_min + eighteen_degree*4)

	for sweep in range(55):
	    pwm.set_pwm(4, 0, servo_min + eighteen_degree*4 +j)
	    time.sleep(0.01)


'''
