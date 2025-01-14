import cv2
import numpy as np
import os

# Function to execute "sudo python left.py"
def move_left():
    print("Moving left")
    subprocess.run(["sudo", "python", "left.py"])
# Function to execute "sudo python right.py"
def move_right():
    print("Moving right")
    subprocess.run(["sudo", "python", "right.py"])

# Function to process the detected objects and control car movement
def process_objects(frame, contours_blue, contours_yellow):
    # Get coordinates of enemy cars
    blue_x = [cv2.boundingRect(contour)[0] for contour in contours_blue]
    yellow_x = [cv2.boundingRect(contour)[0] for contour in contours_yellow]

    # Get coordinates of player car (assuming known position)
    player_x = 60  # Assuming the player's car starts at x-coordinate 60

    # Calculate the time to impact for each enemy car
    CAR_SPEED = 5.0  # Adjust as needed
    time_to_impact_blue = [abs(player_x - blue_pos) / CAR_SPEED for blue_pos in blue_x]
    time_to_impact_yellow = [abs(player_x - yellow_pos) / CAR_SPEED for yellow_pos in yellow_x]

    # Find the nearest enemy cars
    min_time_blue = min(time_to_impact_blue) if time_to_impact_blue else float('inf')
    min_time_yellow = min(time_to_impact_yellow) if time_to_impact_yellow else float('inf')

    # React to the nearest threat
    THRESHOLD_TIME = 1.0  # Adjust as needed
    if min(min_time_blue, min_time_yellow) < THRESHOLD_TIME:
        if min_time_blue < min_time_yellow:
            if player_x < min(blue_x):
                move_right()  # Move right to avoid blue car
            else:
                move_left()  # Move left to avoid blue car
        else:
            if player_x < min(yellow_x):
                move_right()  # Move right to avoid yellow car
            else:
                move_left()  # Move left to avoid yellow car
    else:
        # No immediate threat, prioritize staying in the center lane
        if player_x < 60:
            move_right()  # Move right to stay in the center lane
        elif player_x > 60:
            move_left()   # Move left to stay in the center lane

# Main function
def main():
    # Open the video capture device (change index as needed)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Failed to open camera")
        return

    # Set camera resolution to 640x480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 120)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    # Main loop
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break

        # Convert BGR frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define color ranges for red, blue, and yellow
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([130, 255, 255])
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Threshold the HSV image to obtain masks for each color
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Find contours in the masks
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Process detected objects and control car movement
        process_objects(frame, contours_blue, contours_yellow)

        # Display the processed frame
        cv2.imshow("Object Detection", frame)

        # Check for exit key
        if cv2.waitKey(1) == 27:
            break

    # Release the video capture device
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

