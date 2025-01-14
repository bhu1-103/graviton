import cv2
import numpy as np
import os
import threading

# Function to move the red object left
def move_left():
    os.system("sudo python left.py")

# Function to move the red object right
def move_right():
    os.system("sudo python right.py")

# Function to find and highlight objects of specific colors
def highlight_colors(frame):
    # Convert frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define lower and upper bounds for each color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])
    
    # Threshold the HSV image to get only specific colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Bitwise-AND mask and original image
    res_red = cv2.bitwise_and(frame, frame, mask=mask_red)
    res_yellow = cv2.bitwise_and(frame, frame, mask=mask_yellow)
    res_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)
    
    # Combine the results
    highlighted_image = cv2.addWeighted(res_red, 1, res_yellow, 1, 0)
    highlighted_image = cv2.addWeighted(highlighted_image, 1, res_blue, 1, 0)
    
    return highlighted_image

# Function to simulate falling blue and yellow objects
def simulate_objects():
    while True:
        # Simulate the falling blue and yellow objects (you can add your implementation here)
        pass

# Initialize video capture
cap = cv2.VideoCapture(0)

# Set resolution to 120x240
cap.set(3, 120)
cap.set(4, 240)

# Start thread for simulating falling objects
thread = threading.Thread(target=simulate_objects)
thread.daemon = True
thread.start()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Highlight objects of specific colors
    highlighted_frame = highlight_colors(frame)

    # Display the resulting frame
    cv2.imshow('Game', highlighted_frame)
    
    # Check for user input to move the red object left or right
    key = cv2.waitKey(1)
    if key == ord('a'):
        move_left()
    elif key == ord('d'):
        move_right()
    
    # Exit loop when 'q' is pressed
    if key == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()

