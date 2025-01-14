import cv2
import numpy as np

# Function to highlight objects of a specific color
def highlight_color(frame, lower_color, upper_color, color_name):
    # Convert BGR frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Threshold the HSV image to obtain a mask for the specified color
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw rectangles around the detected objects
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw green rectangles
    
    # Show the frame with highlighted objects
    cv2.imshow(f"{color_name} Objects", frame)


# Open the video capture device (change index as needed)
cap = cv2.VideoCapture(0)

# Main loop
while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break
    
    # Define color ranges for red, green, and blue
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])

    # Highlight red, green, and blue objects in the frame
    highlight_color(frame.copy(), lower_red, upper_red, "Red")
    highlight_color(frame.copy(), lower_green, upper_green, "Green")
    highlight_color(frame.copy(), lower_blue, upper_blue, "Blue")
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close all windows
cap.release()
cv2.destroyAllWindows()

