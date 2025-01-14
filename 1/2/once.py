import cv2
import numpy as np
import subprocess
import time

# Set the desired resolution and section width
width, height = 120, 240
section_width = 30
num_sections = width // section_width

# Define the lanes
lanes = {
    0: (0, 30),
    1: (30, 60),
    2: (60, 90),
    3: (90, 120)
}

# Define the colors for car detection
lower_color = np.array([0, 100, 100])
upper_color = np.array([10, 255, 255])

# Define the color thresholds for blue and yellow cars
blue_lower_color = np.array([100, 100, 100])
blue_upper_color = np.array([120, 255, 255])

yellow_lower_color = np.array([20, 100, 100])
yellow_upper_color = np.array([35, 255, 255])  # Adjusted based on provided color

# Function to draw lane representations
def draw_lanes(frame, lanes):
    for lane, (start, end) in lanes.items():
        cv2.rectangle(frame, (start, 0), (end, height), (255, 255, 255), 1)

# Function to detect the lane of the colored car
def detect_colored_car_lane(frame, lanes, lower_color, upper_color):
    detected_lanes = []
    for lane, (start, end) in lanes.items():
        section = frame[:, start:end]
        mask = cv2.inRange(cv2.cvtColor(section, cv2.COLOR_BGR2HSV), lower_color, upper_color)
        if cv2.countNonZero(mask) > 0:
            detected_lanes.append(lane)
    return detected_lanes

# Function to check if a safe lane is adjacent to the current lane of the red car
def is_adjacent_to_red_car_lane(red_car_lane, safe_lane):
    return abs(red_car_lane - safe_lane) == 1

# Function to execute commands based on the majority of decisions
def execute_command(decisions):
    if decisions.count("right") > decisions.count("left"):
        subprocess.run(["sudo", "python", "right.py"])
    elif decisions.count("right") < decisions.count("left"):
        subprocess.run(["sudo", "python", "left.py"])

# Open a connection to the first webcam
cap = cv2.VideoCapture(0)

# Set the resolution for the webcam capture
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize time for decision delay
last_decision_time = time.time()

# Initialize a list to store decisions
decisions = []

# Flags to track whether left.py and right.py have been executed
left_executed = False
right_executed = False

# Main loop to capture and display the video
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame is read correctly, ret is True
    if ret:
        # Draw lane representations
        draw_lanes(frame, lanes)

        # Detect the lane of the red car
        red_car_lane = detect_colored_car_lane(frame, lanes, lower_color, upper_color)

        # Detect the lane of the blue car
        blue_car_lane = detect_colored_car_lane(frame, lanes, blue_lower_color, blue_upper_color)

        # Detect the lane of the yellow car
        yellow_car_lane = detect_colored_car_lane(frame, lanes, yellow_lower_color, yellow_upper_color)

        # Determine safe lanes to go
        safe_lanes = set(lanes.keys()) - set(red_car_lane + blue_car_lane + yellow_car_lane)

        # Check if it's time to make a decision
        if time.time() - last_decision_time >= 0.2:
            # Determine which direction to choose based on safe lanes
            decision = None
            if red_car_lane:
                for safe_lane in safe_lanes:
                    if is_adjacent_to_red_car_lane(red_car_lane[0], safe_lane):
                        decision = "right" if safe_lane > red_car_lane[0] else "left"
                        break
            
            # Add decision to the list
            if decision:
                decisions.append(decision)

            # If there are enough decisions, execute the majority decision
            if len(decisions) >= 5:
                if decisions.count("left") > 0 and not left_executed:
                    subprocess.run(["sudo", "python", "left.py"])
                    left_executed = True
                elif decisions.count("right") > 0 and not right_executed:
                    subprocess.run(["sudo", "python", "right.py"])
                    right_executed = True

            # Update the time of the last decision
            last_decision_time = time.time()

        # Display the frame
        cv2.imshow('Road Fighter', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

