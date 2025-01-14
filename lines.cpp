#include <opencv2/opencv.hpp>

using namespace cv;

void detectLines() {
    VideoCapture cap(0);  // Initialize camera (adjust index if using external camera)

    cap.set(CAP_PROP_FRAME_WIDTH, 640);
    cap.set(CAP_PROP_FRAME_HEIGHT, 480);

    while (true) {
        Mat frame;
        cap.read(frame);  // Read frame from the camera

        if (frame.empty()) {
            break;
        }

        Mat gray;
        cvtColor(frame, gray, COLOR_BGR2GRAY);

        GaussianBlur(gray, gray, Size(5, 5), 0);

        // Detect edges using Canny edge detector
        Mat edges;
        Canny(gray, edges, 50, 150);

        // Perform Hough line detection
        std::vector<Vec4i> lines;
        HoughLinesP(edges, lines, 1, CV_PI / 180, 100, 100, 10);

        if (!lines.empty()) {
            for (size_t i = 0; i < lines.size(); i++) {
                Vec4i l = lines[i];
                // Draw lines on the original frame
                line(frame, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0, 255, 0), 2);
            }
        }

        // Display the resulting frame
        imshow("Frame", frame);

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
    // Call the function to detect lines
    detectLines();

    return 0;
}

