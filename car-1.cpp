#include <opencv2/opencv.hpp>
#include <iostream>
#include <cstdlib>  // For system()

void move_left() {
    std::cout << "Moving left" << std::endl;
    system("sudo python left.py");
}

void move_right() {
    std::cout << "Moving right" << std::endl;
    system("sudo python right.py");
}

void process_objects(cv::Mat& frame, const std::vector<std::vector<cv::Point>>& contours_blue, 
                     const std::vector<std::vector<cv::Point>>& contours_yellow) {
    std::vector<int> blue_x, yellow_x;
    for (const auto& contour : contours_blue) {
        cv::Rect rect = cv::boundingRect(contour);
        blue_x.push_back(rect.x);
    }
    for (const auto& contour : contours_yellow) {
        cv::Rect rect = cv::boundingRect(contour);
        yellow_x.push_back(rect.x);
    }

    const int num_lanes = 8; // Dividing the lanes into 8 segments
    std::vector<int> lane_occupancy(num_lanes, 0); // Initialize with 0 (lane is empty)

    // Update lane occupancy based on detected objects
    for (int x : blue_x) {
        int lane = x * num_lanes / frame.cols; // Map x-coordinate to lane
        lane_occupancy[lane]++;
    }
    for (int x : yellow_x) {
        int lane = x * num_lanes / frame.cols; // Map x-coordinate to lane
        lane_occupancy[lane]++;
    }

    // Determine which lane to move based on occupancy
    int min_lane_occupancy = INT_MAX;
    int optimal_lane = -1;

    for (int i = 0; i < num_lanes; ++i) {
        if (lane_occupancy[i] < min_lane_occupancy) {
            min_lane_occupancy = lane_occupancy[i];
            optimal_lane = i;
        }
    }

    // If no objects detected, do not move
    if (min_lane_occupancy == 0) {
        std::cout << "No objects detected, maintaining current lane." << std::endl;
        return;
    }

    // Otherwise, move the car to the optimal lane
    int current_lane = 3; // Assuming the car starts in the middle lane
    if (optimal_lane < current_lane) {
        move_left();
    } else if (optimal_lane > current_lane) {
        move_right();
    } else {
        std::cout << "Already in the optimal lane." << std::endl;
    }
}

int main() {
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cerr << "Error: Failed to open camera" << std::endl;
        return -1;
    }

    cap.set(cv::CAP_PROP_FRAME_WIDTH, 120);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 280);

    while (true) {
        cv::Mat frame;
        cap >> frame;

        cv::Mat hsv;
        cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);

        cv::Scalar lower_red(0, 100, 100);
        cv::Scalar upper_red(10, 255, 255);
        cv::Scalar lower_blue(100, 100, 100);
        cv::Scalar upper_blue(130, 255, 255);
        cv::Scalar lower_yellow(20, 100, 100);
        cv::Scalar upper_yellow(30, 255, 255);

        cv::Mat mask_red, mask_blue, mask_yellow;
        cv::inRange(hsv, lower_red, upper_red, mask_red);
        cv::inRange(hsv, lower_blue, upper_blue, mask_blue);
        cv::inRange(hsv, lower_yellow, upper_yellow, mask_yellow);

        std::vector<std::vector<cv::Point>> contours_red, contours_blue, contours_yellow;
        cv::findContours(mask_red, contours_red, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
        cv::findContours(mask_blue, contours_blue, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
        cv::findContours(mask_yellow, contours_yellow, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

        for (const auto& contour : contours_red) {
            cv::Rect rect = cv::boundingRect(contour);
            cv::rectangle(frame, rect, cv::Scalar(0, 0, 255), 2);
            std::cout << "Red Object X-coordinate: " << rect.x << std::endl;
        }
        for (const auto& contour : contours_blue) {
            cv::Rect rect = cv::boundingRect(contour);
            cv::rectangle(frame, rect, cv::Scalar(255, 0, 0), 2);
            std::cout << "Blue Object X-coordinate: " << rect.x << std::endl;
        }
        for (const auto& contour : contours_yellow) {
            cv::Rect rect = cv::boundingRect(contour);
            cv::rectangle(frame, rect, cv::Scalar(0, 255, 255), 2);
            std::cout << "Yellow Object X-coordinate: " << rect.x << std::endl;
        }

        process_objects(frame, contours_blue, contours_yellow);

        cv::imshow("Object Detection", frame);

        if (cv::waitKey(1) == 27) {
            break;
        }
    }

    cap.release();
    cv::destroyAllWindows();

    return 0;
}

