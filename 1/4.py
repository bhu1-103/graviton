import cv2

# Set the desired resolution and section width
width, height = 120, 240
section_width = 30
num_sections = width // section_width

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
        # Divide the frame into sections and draw black borders
        for i in range(num_sections - 1):
            cv2.line(frame, (section_width * (i + 1), 0), (section_width * (i + 1), height), (0, 0, 0), 1)

        # Display the frame
        cv2.imshow('Live Video', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

