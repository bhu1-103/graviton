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

    int player_x = 60;

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
        // No nearby enemy cars, maintain current direction or accelerate
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

