import RPi.GPIO as GPIO
import time

# Ultrasonic sensor pins
TRIG_PIN = 17
ECHO_PIN = 18

# GPIO setup
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def obstacle_detected():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    start_time = time.time()
    stop_time = time.time()
    
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()
    
    distance = (stop_time - start_time) * 34300 / 2  # Distance in cm
    return distance < 30  # Obstacle detected if distance < 30 cm
