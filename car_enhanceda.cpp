#include <opencv2/opencv.hpp>
#include <iostream>
#include <cstdlib>  // For system()

std::vector<std::vector<cv::Point>> contours_blue, contours_yellow; // Declare outside main()

void move_left() {
    std::cout << "Moving left" << std::endl;
    system("sudo python left.py");
}

void move_right() {
    std::cout << "Moving right" << std::endl;
    system("sudo python right.py");
}

void move_forward() {
    // Assume there's a function to move the car forward
    std::cout << "Moving forward" << std::endl;
}

void process_objects(cv::Mat& frame) {
    std::vector<int> blue_x, yellow_x;
    for (const auto& contour : contours_blue) {
        cv::Rect rect = cv::boundingRect(contour);
        blue_x.push_back(rect.x);
    }
    for (const auto& contour : contours_yellow) {
        cv::Rect rect = cv::boundingRect(contour);
        yellow_x.push_back(rect.x);
    }

    int player_x = 60;  // Assuming the red car's starting position

    std::vector<int> distance_blue, distance_yellow;
    for (int x : blue_x) {
        distance_blue.push_back(std::abs(player_x - x));
    }
    for (int x : yellow_x) {
        distance_yellow.push_back(std::abs(player_x - x));
    }

    const int THRESHOLD_DISTANCE = 15;  
    if (!distance_blue.empty() && *std::min_element(distance_blue.begin(), distance_blue.end()) < THRESHOLD_DISTANCE) {
        move_right();  
    } else if (!distance_yellow.empty() && *std::min_element(distance_yellow.begin(), distance_yellow.end()) < THRESHOLD_DISTANCE) {
        move_left();  
    } else {
        move_forward();  // Move forward if no obstacles detected
    }
}

int main() {
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cerr << "Error: Failed to open camera" << std::endl;
        return -1;
    }

    cap.set(cv::CAP_PROP_FRAME_WIDTH, 120);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 240);

    while (true) {
        cv::Mat frame;
        cap >> frame;

        cv::Mat hsv;
        cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);

        // Assuming the color ranges for the grey road
        cv::Scalar lower_grey(0, 0, 100);
        cv::Scalar upper_grey(179, 50, 255);

        cv::Mat mask_grey;
        cv::inRange(hsv, lower_grey, upper_grey, mask_grey);

        std::vector<std::vector<cv::Point>> contours_grey;
        cv::findContours(mask_grey, contours_grey, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

        // Process grey road
        if (!contours_grey.empty()) {
            cv::Rect road_rect = cv::boundingRect(contours_grey[0]);
            int road_center_x = road_rect.x + road_rect.width / 2;

            // Assuming the red car's width is known
            int red_car_width = 20;  

            int offset = road_center_x - (frame.cols / 2) - (red_car_width / 2);

            if (offset > 0) {
                move_right();  // Adjust right
            } else if (offset < 0) {
                move_left();   // Adjust left
            } else {
                move_forward(); // Stay in the middle
            }
        }

        process_objects(frame);

        cv::imshow("Object Detection", frame);

        if (cv::waitKey(1) == 27) {
            break;
        }
    }

    cap.release();
    cv::destroyAllWindows();

    return 0;
}

