import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import time
from threading import Thread

# Flask setup
app = Flask(__name__)

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Motor pins
MOTOR_LEFT_FORWARD = 23
MOTOR_LEFT_BACKWARD = 24
MOTOR_RIGHT_FORWARD = 27
MOTOR_RIGHT_BACKWARD = 22

# Ultrasonic sensor pins
TRIG_PIN = 17
ECHO_PIN = 18

# Motor setup
GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)

# Ultrasonic sensor setup
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialize variables
mode = "manual"  # Modes: manual, autonomous
target_bbox = None

# Load EfficientDet model
model = tf.saved_model.load("efficientdet_d0_saved_model")  # Update path to your EfficientDet model
detect_fn = model.signatures['serving_default']

# Obstacle avoidance function
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

# Motor control functions
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

# Human following function
def follow_human():
    global target_bbox
    cap = cv2.VideoCapture(0)
    
    while True:
        if mode == "autonomous":
            ret, frame = cap.read()
            if not ret:
                continue

            input_tensor = tf.convert_to_tensor([frame])
            detections = detect_fn(input_tensor)
            
            # Extract bounding boxes
            bboxes = detections['detection_boxes'][0].numpy()
            scores = detections['detection_scores'][0].numpy()
            classes = detections['detection_classes'][0].numpy().astype(np.int32)
            
            for i in range(len(scores)):
                if scores[i] > 0.5:  # Threshold confidence
                    ymin, xmin, ymax, xmax = bboxes[i]
                    x_center = (xmin + xmax) / 2
                    y_center = (ymin + ymax) / 2

                    # Control logic
                    if obstacle_detected():
                        stop()
                    elif x_center < 0.4:
                        turn_left()
                    elif x_center > 0.6:
                        turn_right()
                    else:
                        move_forward()
                else:
                    stop()

# Flask routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/mode', methods=['POST'])
def set_mode():
    global mode
    data = request.json
    mode = data.get("mode", "manual")
    return jsonify({"status": "success", "mode": mode})

@app.route('/manual_control', methods=['POST'])
def manual_control():
    data = request.json
    action = data.get("action")
    
    if action == "forward":
        move_forward()
    elif action == "backward":
        move_backward()
    elif action == "left":
        turn_left()
    elif action == "right":
        turn_right()
    elif action == "stop":
        stop()
    
    return jsonify({"status": "success"})

if __name__ == "__main__":
    try:
        Thread(target=follow_human).start()
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()
