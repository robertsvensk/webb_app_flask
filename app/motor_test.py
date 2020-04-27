# Drive DC-pump
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

pwma = 7
ain2 = 11
ain1 = 12
stby = 13

# Setup pins
GPIO.setup(pwma,GPIO.OUT)  #PWMA
GPIO.setup(ain2,GPIO.OUT) #AIN2
GPIO.setup(ain1,GPIO.OUT) #AIN1
GPIO.setup(stby,GPIO.OUT) #STBY

# Drive the motor
GPIO.output(ain1, GPIO.HIGH)  # Set AIN1
GPIO.output(ain2, GPIO.LOW)   # Set AIN2

# Set the motor speed
GPIO.output(pwma, GPIO.HIGH)

# Disable standby
GPIO.output(stby, GPIO.HIGH)

print('hello')

# Wait 1 second
time.sleep(1)

GPIO.output(ain1, GPIO.LOW)
GPIO.output(ain2, GPIO.LOW)
GPIO.output(pwma, GPIO.LOW)
GPIO.output(stby, GPIO.LOW)
