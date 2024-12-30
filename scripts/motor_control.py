import RPi.GPIO as GPIO

# Motor GPIO pins
MOTOR_LEFT_FORWARD = 23
MOTOR_LEFT_BACKWARD = 24
MOTOR_RIGHT_FORWARD = 27
MOTOR_RIGHT_BACKWARD = 22

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)

def move_forward():
    GPIO.output(MOTOR_LEFT_FORWARD, True)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_FORWARD, True)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)

def move_backward():
    GPIO.output(MOTOR_LEFT_FORWARD, False)
    GPIO.output(MOTOR_LEFT_BACKWARD, True)
    GPIO.output(MOTOR_RIGHT_FORWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, True)

def turn_left():
    GPIO.output(MOTOR_LEFT_FORWARD, False)
    GPIO.output(MOTOR_LEFT_BACKWARD, True)
    GPIO.output(MOTOR_RIGHT_FORWARD, True)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)

def turn_right():
    GPIO.output(MOTOR_LEFT_FORWARD, True)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_FORWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, True)

def stop():
    GPIO.output(MOTOR_LEFT_FORWARD, False)
    GPIO.output(MOTOR_LEFT_BACKWARD, False)
    GPIO.output(MOTOR_RIGHT_FORWARD, False)
    GPIO.output(MOTOR_RIGHT_BACKWARD, False)
