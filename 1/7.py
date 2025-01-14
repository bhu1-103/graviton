import cv2
import numpy as np

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

# Define the color for red car detection
red_lower_color = np.array([0, 100, 100])
red_upper_color = np.array([10, 255, 255])

# Function to detect the lane of the front car
def detect_lane(frame, lanes):
    lane_center = width // 2
    for lane, (start, end) in lanes.items():
        section = frame[:, start:end]
        mask = cv2.inRange(cv2.cvtColor(section, cv2.COLOR_BGR2HSV), lower_color, upper_color)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cnt = max(contours, key=cv2.contourArea)
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                if start <= cX <= end:
                    return lane
    return None

# Function to detect the lane of the red car
def detect_red_car_lane(frame, lanes):
    for lane, (start, end) in lanes.items():
        section = frame[:, start:end]
        mask = cv2.inRange(cv2.cvtColor(section, cv2.COLOR_BGR2HSV), red_lower_color, red_upper_color)
        if cv2.countNonZero(mask) > 0:
            return lane
    return None

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
        # Divide the frame into sections and draw lane borders
        for i in range(num_sections):
            cv2.line(frame, (section_width * (i + 1), 0), (section_width * (i + 1), height), (0, 0, 0), 1)

        # Detect the lane of the red car
        red_car_lane = detect_red_car_lane(frame, lanes)

        # Print the lane of the red car
        if red_car_lane is not None:
            print("Red car is in lane:", red_car_lane)
        else:
            print("Red car not detected")

        # Display the frame
        cv2.imshow('Road Fighter', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

