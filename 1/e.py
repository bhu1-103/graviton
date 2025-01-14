import cv2
import numpy as np
import subprocess

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

# Function to execute commands based on safe lanes
def execute_command(direction):
    if direction == "right":
        subprocess.run(["sudo", "python", "right.py"])
    elif direction == "left":
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

# Main loop to capture and display the video
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame is read correctly, ret is True
    if ret:
        # Draw lane representations
        draw_lanes(frame, lanes)

        # Detect the lane of the blue car
        blue_car_lane = detect_colored_car_lane(frame, lanes, blue_lower_color, blue_upper_color)

        # Detect the lane of the yellow car
        yellow_car_lane = detect_colored_car_lane(frame, lanes, yellow_lower_color, yellow_upper_color)

        # Determine if a blue or yellow car is present
        if blue_car_lane or yellow_car_lane:
            if blue_car_lane:
                print("Blue car detected!")
            if yellow_car_lane:
                print("Yellow car detected!")
            # Move the car left or right based on the color detected
            if yellow_car_lane and yellow_car_lane[0] + 1 in lanes.keys():
                print("Moving right to avoid the yellow car")
                execute_command("right")
            elif blue_car_lane and blue_car_lane[0] - 1 in lanes.keys():
                print("Moving left to avoid the blue car")
                execute_command("left")

        # Display the frame
        cv2.imshow('Road Fighter', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

