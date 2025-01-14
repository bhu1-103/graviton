#include <opencv2/opencv.hpp>

int main() {
    // Open the video capture device (change index as needed)
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cerr << "Error: Failed to open camera" << std::endl;
        return -1;
    }

    // Set camera resolution to 640x480
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 120);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 240);

    // Main loop
    while (true) {
        // Capture a frame from the camera
        cv::Mat frame;
        cap >> frame;

        // Convert BGR frame to HSV color space
        cv::Mat hsv;
        cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);

        // Define color ranges for red, blue, and yellow
        cv::Scalar lower_red(0, 100, 100);
        cv::Scalar upper_red(10, 255, 255);
        cv::Scalar lower_blue(100, 100, 100);
        cv::Scalar upper_blue(130, 255, 255);
        cv::Scalar lower_yellow(20, 100, 100);
        cv::Scalar upper_yellow(30, 255, 255);

        // Threshold the HSV image to obtain masks for each color
        cv::Mat mask_red, mask_blue, mask_yellow;
        cv::inRange(hsv, lower_red, upper_red, mask_red);
        cv::inRange(hsv, lower_blue, upper_blue, mask_blue);
        cv::inRange(hsv, lower_yellow, upper_yellow, mask_yellow);

        // Find contours in the masks
        std::vector<std::vector<cv::Point>> contours_red, contours_blue, contours_yellow;
        cv::findContours(mask_red, contours_red, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
        cv::findContours(mask_blue, contours_blue, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
        cv::findContours(mask_yellow, contours_yellow, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

        // Draw rectangles around the detected cars
        for (const auto& contour : contours_red) {
            cv::Rect rect = cv::boundingRect(contour);
            cv::rectangle(frame, rect, cv::Scalar(0, 0, 255), 2); // Draw red rectangles
        }
        for (const auto& contour : contours_blue) {
            cv::Rect rect = cv::boundingRect(contour);
            cv::rectangle(frame, rect, cv::Scalar(255, 0, 0), 2); // Draw blue rectangles
        }
        for (const auto& contour : contours_yellow) {
            cv::Rect rect = cv::boundingRect(contour);
            cv::rectangle(frame, rect, cv::Scalar(0, 255, 255), 2); // Draw yellow rectangles
        }

        // Display the processed frame
        cv::imshow("Object Detection", frame);

        // Check for exit key
        if (cv::waitKey(1) == 27) {
            break;
        }
    }

    // Release the video capture device
    cap.release();
    cv::destroyAllWindows();

    return 0;
}
