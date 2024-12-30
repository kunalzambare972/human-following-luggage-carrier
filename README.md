# Human Following Luggage Carrier

## Overview
This project involves the development of a human-following luggage carrier using a Raspberry Pi. The carrier utilizes a Raspberry Pi Camera v2.1 for human detection, EfficientDet for object detection, ultrasonic sensors for obstacle avoidance, and L298N motor drivers for motor control. The system supports both manual and autonomous modes, and a Flask-based GUI allows users to interact with the robot.

---

## Features
- **Autonomous Human Following:**
  The robot autonomously follows a specific human based on their back profile captured by the camera.

- **Manual Control:**
  Users can control the robot manually via the GUI.

- **Obstacle Avoidance:**
  Ultrasonic sensors detect obstacles and prevent collisions.

- **Flask GUI:**
  A simple web interface for switching between modes and controlling the robot manually.

---

## Components
### Hardware
- **Raspberry Pi (any version with GPIO support)**
- **Raspberry Pi Camera v2.1**
- **4 DC Motors**
- **L298N Motor Driver**
- **Ultrasonic Sensor (HC-SR04)**
- **Power Supply**

### Software
- **Python**
- **Flask (for GUI)**
- **EfficientDet (for human detection)**
- **TensorFlow (for object detection)**
- **OpenCV (for video processing)**

---

---

## Setup Instructions

### 1. Hardware Setup
1. Connect the motors to the L298N motor driver module.
2. Connect the L298N module to the Raspberry Pi GPIO pins as follows:
   - **Motor Left Forward:** GPIO 23
   - **Motor Left Backward:** GPIO 24
   - **Motor Right Forward:** GPIO 27
   - **Motor Right Backward:** GPIO 22
3. Connect the ultrasonic sensor to the Raspberry Pi GPIO pins:
   - **Trigger Pin:** GPIO 17
   - **Echo Pin:** GPIO 18
4. Attach the Raspberry Pi Camera v2.1 to the CSI interface of the Raspberry Pi.
5. Power up the Raspberry Pi and ensure all connections are secure.

### 2. Software Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/human_following_luggage_carrier.git
   cd human_following_luggage_carrier
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Access the GUI:
   Open a browser and navigate to `http://<raspberry_pi_ip>:5000`.

---

## Usage

### Manual Mode
1. Select "Manual Mode" on the GUI.
2. Use the direction buttons to control the robot:
   - **Forward**
   - **Backward**
   - **Left**
   - **Right**
   - **Stop**

### Autonomous Mode
1. Select "Autonomous Mode" on the GUI.
2. The robot will start following the detected human based on the back profile captured by the camera.

---

## Scripts

### 1. `motor_control.py`
Handles motor operations like moving forward, backward, turning left, and turning right.

### 2. `human_tracking.py`
Uses EfficientDet and TensorFlow to detect and track the human target.

### 3. `obstacle_avoidance.py`
Uses the HC-SR04 ultrasonic sensor to detect obstacles and avoid collisions.

### 4. `routes.py`
Defines Flask routes for switching between modes and handling manual control commands.

---

## Model Details
- **EfficientDet:** Pre-trained EfficientDet D0 model is used for human detection and tracking.

- **Bounding Box Analysis:** The center of the detected bounding box determines the direction the robot should move.

---

## Dependencies

The following Python libraries are required:
```plaintext
flask
opencv-python
opencv-python-headless
tensorflow
numpy
RPi.GPIO
```
Install them using:
```bash
pip install -r requirements.txt
```

---

## Troubleshooting

1. **No Camera Feed:**
   - Ensure the Raspberry Pi Camera is enabled in the `raspi-config` settings.
   - Check the connection of the camera to the Raspberry Pi.

2. **Motors Not Moving:**
   - Verify the wiring between the motor driver and the Raspberry Pi.
   - Check the power supply for the motors.

3. **Ultrasonic Sensor Not Working:**
   - Ensure the trigger and echo pins are connected to the correct GPIO pins.
   - Verify the sensor's placement for proper obstacle detection.

---

## Future Enhancements
- Add multi-human detection and user-specific following using a user profile database.
- Implement a mobile app interface for better control.
- Enhance obstacle avoidance using LiDAR or additional sensors.

---

## License
This project is licensed under the MIT License.

---

