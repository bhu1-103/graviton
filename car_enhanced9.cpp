#include <opencv2/opencv.hpp>
#include <iostream>
#include <cstdlib>  // For system()

// Function to execute "sudo python left.py"
void move_left() {
    std::cout << "Moving left" << std::endl;
    system("sudo python left.py");
}

// Function to execute "sudo python right.py"
void move_right() {
    std::cout << "Moving right" << std::endl;
    system("sudo python right.py");
}

// Function to process the detected objects and control car movement
void process_objects(cv::Mat& frame, const std::vector<std::vector<cv::Point>>& contours_blue,
                     const std::vector<std::vector<cv::Point>>& contours_yellow) {
    // Get coordinates of enemy cars
    std::vector<int> blue_x, yellow_x;
    for (const auto& contour : contours_blue) {
        cv::Rect rect = cv::boundingRect(contour);
        blue_x.push_back(rect.x);
    }
    for (const auto& contour : contours_yellow) {
        cv::Rect rect = cv::boundingRect(contour);
        yellow_x.push_back(rect.x);
    }

    // Get coordinates of player car (assuming known position)
    int player_x = 60;  // Assuming the player's car starts at x-coordinate 60

    // Calculate the time to impact for each enemy car
    std::vector<double> time_to_impact_blue, time_to_impact_yellow;
    const double CAR_SPEED = 5.0;  // Adjust as needed
    for (int blue_pos : blue_x) {
        double time = static_cast<double>(std::abs(player_x - blue_pos)) / CAR_SPEED;
        time_to_impact_blue.push_back(time);
    }
    for (int yellow_pos : yellow_x) {
        double time = static_cast<double>(std::abs(player_x - yellow_pos)) / CAR_SPEED;
        time_to_impact_yellow.push_back(time);
    }

    // Find the nearest enemy cars
    double min_time_blue = *std::min_element(time_to_impact_blue.begin(), time_to_impact_blue.end());
    double min_time_yellow = *std::min_element(time_to_impact_yellow.begin(), time_to_impact_yellow.end());

    // React to the nearest threat
    const double THRESHOLD_TIME = 1.0;  // Adjust as needed
    if (min_time_blue < THRESHOLD_TIME || min_time_yellow < THRESHOLD_TIME) {
        // There is an immediate threat
        if (min_time_blue < min_time_yellow) {
            // React to the nearest blue car
            int nearest_blue_index = std::min_element(time_to_impact_blue.begin(), time_to_impact_blue.end()) - time_to_impact_blue.begin();
            if (player_x < blue_x[nearest_blue_index]) {
                move_right();  // Move right to avoid blue car
            } else {
                move_left();  // Move left to avoid blue car
            }
        } else {
            // React to the nearest yellow car
            int nearest_yellow_index = std::min_element(time_to_impact_yellow.begin(), time_to_impact_yellow.end()) - time_to_impact_yellow.begin();
            if (player_x < yellow_x[nearest_yellow_index]) {
                move_right();  // Move right to avoid yellow car
            } else {
                move_left();  // Move left to avoid yellow car
            }
        }
    } else {
        // No immediate threat, prioritize staying in the center lane
        if (player_x < 60) {
            move_right();  // Move right to stay in the center lane
        } else if (player_x > 60) {
            move_left();   // Move left to stay in the center lane
        }
    }
}


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

        // Draw rectangles around the detected objects and print x-coordinates
        for (const auto& contour : contours_red) {
            cv::Rect rect = cv::boundingRect(contour);
            cv::rectangle(frame, rect, cv::Scalar(0, 0, 255), 2); // Draw red rectangles
            std::cout << "Red Object X-coordinate: " << rect.x << std::endl;
        }
        for (const auto& contour : contours_blue) {
            cv::Rect rect = cv::boundingRect(contour);
            cv::rectangle(frame, rect, cv::Scalar(255, 0, 0), 2); // Draw blue rectangles
            std::cout << "Blue Object X-coordinate: " << rect.x << std::endl;
        }
        for (const auto& contour : contours_yellow) {
            cv::Rect rect = cv::boundingRect(contour);
            cv::rectangle(frame, rect, cv::Scalar(0, 255, 255), 2); // Draw yellow rectangles
            std::cout << "Yellow Object X-coordinate: " << rect.x << std::endl;
        }

        // Process detected objects and control car movement
        process_objects(frame, contours_blue, contours_yellow);

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
