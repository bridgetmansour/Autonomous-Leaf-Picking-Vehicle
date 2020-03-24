from v2 import *
import RPi.GPIO as GPIO
import time 
import numpy as np
import serial
from picamera import PiCamera

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(36, GPIO.OUT) #baseframe
GPIO.setup(38, GPIO.OUT) #ANGLE1
GPIO.setup(40, GPIO.OUT) #ANGLE2
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)

q = GPIO.PWM(36, 50) #baseframe
s = GPIO.PWM(38, 50) #ANGLE1
t = GPIO.PWM(40, 50) #ANGLE2
in1 = 16
in2 = 18

time.sleep(5)

q.start(6.0)
s.start(7.5)
t.start(7.5)

def SetAngle(baseangle):
    #isLeaf = True
    if K == True:
        
        time.sleep(2)
    
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
     
        q.ChangeDutyCycle(6.0)
        time.sleep(2.0)
        s.ChangeDutyCycle(7.5)
        time.sleep(2.0)
        t.ChangeDutyCycle(6.0)
        time.sleep(2.0)

        #print("x and y coordinates are:",x,y)
        
        #angle1 = np.degrees(np.arctan2(y,x))
        angle1 = baseangle
        angle2 = 185
        angle3 = 95
        
        print("angle1, angle2 and angle3 are:",angle1, angle2, angle3)
        
        time.sleep(2)

        duty1 = angle1*(10.5/180) + 1.5
        print("duty1:",duty1)
        if duty1 < 0:
            #duty1 = duty1 + 99
            duty1 = np.abs(duty1)
        q.ChangeDutyCycle(duty1)
        time.sleep(2.0)
        
        duty2 = angle2*(10.5/180) + 1.5
        print("duty2:",duty2)
        if duty2 < 0:
            duty2 = 100.0 - duty2
        s.ChangeDutyCycle(duty2)
        time.sleep(2.0)
        
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        
        duty3 = angle3*(10.5/180) + 1.5
        print("duty3:",duty3)
        if duty3 < 0:
            duty3 = 100.0 - duty3 
        t.ChangeDutyCycle(duty3)
        time.sleep(1.0)
    
        #activate vacuum

        print("Final values of duty1, duty2, duty3, duty4 are:",duty1,duty2,duty3) 
        HomeAngle()
        return
    else:
        q.stop()
        r.stop()
        s.stop()
        

def HomeAngle():
  
    angle1 = 153.43
    angle2 = 45
    angle3 = 90
    
    print(angle1, angle2, angle3)
    
    s.ChangeDutyCycle(6.0)
    time.sleep(2.0)
    #t.ChangeDutyCycle(2.0)
    #time.sleep(2.0)
    q.ChangeDutyCycle(10.4503)
    time.sleep(2.0)
  
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    
    return

try:
    SetAngle(D)

finally:
    q.stop()
    s.stop()
    t.stop()
    GPIO.cleanup()
    print('done')