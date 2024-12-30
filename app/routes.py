from flask import render_template, request, jsonify
from app import app
from scripts.motor_control import move_forward, move_backward, turn_left, turn_right, stop
import threading

# Global variables
mode = "manual"  # Modes: manual, autonomous

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

# Background thread to handle autonomous mode
def autonomous_mode():
    from scripts.human_tracking import follow_human
    follow_human()

# Start autonomous mode thread
thread = threading.Thread(target=autonomous_mode)
thread.daemon = True
thread.start()
