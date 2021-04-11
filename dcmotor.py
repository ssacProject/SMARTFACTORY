

import Jetson.GPIO as GPIO
import time

# TEGRA_SOC, LCD_BL_PW pin 32

count=0

def go():
    try:
        global count
       	GPIO.setmode(GPIO.TEGRA_SOC)
       	GPIO.setup('LCD_BL_PW', GPIO.OUT, initial=GPIO.HIGH)
       	#print("dcmotor run")
        
        count=count+1
        if count % 3==1:
       	    GPIO.output('LCD_BL_PW', GPIO.HIGH)
            #print("high")
        else:#for _ in range(25):		
  	#   GPIO.output('LCD_BL_PW', GPIO.HIGH)
            GPIO.output('LCD_BL_PW', GPIO.LOW)
            #print("low")

    finally:
        GPIO.cleanup()

def stop():
    try:
       	GPIO.setmode(GPIO.TEGRA_SOC)
       	GPIO.setup('LCD_BL_PW', GPIO.OUT, initial=GPIO.HIGH)
       	print("dcmotor stop")
       	GPIO.output('LCD_BL_PW', GPIO.LOW)
       	time.sleep(0.1)

    finally:
            GPIO.cleanup()
'''
if __name__ == '__main__':
    go()
    #stop()
'''
