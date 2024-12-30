import cv2
import tensorflow as tf
from scripts.motor_control import move_forward, stop, turn_left, turn_right
from scripts.obstacle_avoidance import obstacle_detected

# Load EfficientDet model
model = tf.saved_model.load("models/efficientdet_d0_saved_model")
detect_fn = model.signatures['serving_default']

def follow_human():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        input_tensor = tf.convert_to_tensor([frame])
        detections = detect_fn(input_tensor)

        # Extract bounding boxes
        bboxes = detections['detection_boxes'][0].numpy()
        scores = detections['detection_scores'][0].numpy()
        
        for i, score in enumerate(scores):
            if score > 0.5:  # Confidence threshold
                x_center = (bboxes[i][1] + bboxes[i][3]) / 2

                if obstacle_detected():
                    stop()
                elif x_center < 0.4:
                    turn_left()
                elif x_center > 0.6:
                    turn_right()
                else:
                    move_forward()
