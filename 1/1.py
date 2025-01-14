import cv2
import numpy as np

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

# Initialize video capture
cap = cv2.VideoCapture(0)

# Set resolution to 120x240
cap.set(3, 120)
cap.set(4, 240)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Highlight objects of specific colors
    highlighted_frame = highlight_colors(frame)

    # Display the resulting frame
    cv2.imshow('Highlighted Objects', highlighted_frame)
    
    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()

