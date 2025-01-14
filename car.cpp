#include <opencv2/opencv.hpp>

using namespace cv;

void detectRedObjects() {
    VideoCapture cap(0);  // Initialize camera (adjust index if using external camera)

    cap.set(CAP_PROP_FRAME_WIDTH, 640);
    cap.set(CAP_PROP_FRAME_HEIGHT, 480);

    while (true) {
        Mat frame;
        cap.read(frame);  // Read frame from the camera

        if (frame.empty()) {
            break;
        }

        // Convert BGR image to HSV
        Mat hsv;
        cvtColor(frame, hsv, COLOR_BGR2HSV);

        // Define lower and upper bounds for red color in HSV
        Scalar lower_red = Scalar(0, 100, 100);  // Lower bound (adjust as needed)
        Scalar upper_red = Scalar(10, 255, 255); // Upper bound (adjust as needed)

        // Threshold the HSV image to get only red color
        Mat mask;
        inRange(hsv, lower_red, upper_red, mask);

        // Bitwise AND the mask with the original image
        Mat res;
        bitwise_and(frame, frame, res, mask);

        // Display the resulting frame
        imshow("Car", res);

        // Exit if 'q' is pressed
        if (waitKey(1) == 'q') {
            break;
        }
    }

    // Release the camera and close all windows
    cap.release();
    destroyAllWindows();
}

// Entry point
int main() {
    // Call the function to detect red objects
    detectRedObjects();

    return 0;
}

