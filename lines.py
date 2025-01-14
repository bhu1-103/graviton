import cv2
import numpy as np

def detect_lines():
    cap = cv2.VideoCapture(0)  # Initialize camera (adjust index if using external camera)
    
    # Set camera resolution to 640 x 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    
    while True:
        ret, frame = cap.read()  # Read frame from the camera
        
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Detect edges using Canny edge detector
        edges = cv2.Canny(blurred, 50, 150)
        
        # Perform Hough line detection
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # Draw lines on the original frame
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function to detect lines
detect_lines()

