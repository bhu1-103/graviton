#include <opencv2/opencv.hpp>

using namespace cv;

void detectColorObjects() {
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
        Scalar lower_red = Scalar(0, 100, 100);   // Lower bound for red (adjust as needed)
        Scalar upper_red = Scalar(10, 255, 255);  // Upper bound for red (adjust as needed)

        // Define lower and upper bounds for yellow color in HSV
        Scalar lower_yellow = Scalar(20, 100, 100);  // Lower bound for yellow (adjust as needed)
        Scalar upper_yellow = Scalar(30, 255, 255);  // Upper bound for yellow (adjust as needed)

        // Define lower and upper bounds for blue color in HSV
        Scalar lower_blue = Scalar(100, 100, 100);  // Lower bound for blue (adjust as needed)
        Scalar upper_blue = Scalar(130, 255, 255); // Upper bound for blue (adjust as needed)

        // Threshold the HSV image to get only red, yellow, and blue colors
        Mat mask_red, mask_yellow, mask_blue;
        inRange(hsv, lower_red, upper_red, mask_red);
        inRange(hsv, lower_yellow, upper_yellow, mask_yellow);
        inRange(hsv, lower_blue, upper_blue, mask_blue);

        // Bitwise OR operation to combine masks for red, yellow, and blue colors
        Mat mask_combined = mask_red | mask_yellow | mask_blue;

        // Bitwise AND the mask with the original image
        Mat res;
        bitwise_and(frame, frame, res, mask_combined);

        // Display the resulting frame
        imshow("Color Objects", res);

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
    // Call the function to detect red, yellow, and blue objects
    detectColorObjects();

    return 0;
}

