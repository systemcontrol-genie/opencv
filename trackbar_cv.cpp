#include <iostream>
#include <opencv2/opencv.hpp>

void one_level_change(int pos, void* usrdata);

int main(void)
{
	cv::Mat img = cv::Mat::zeros(400, 400, CV_8UC1);
	cv::namedWindow("img");
	cv::createTrackbar("level", "img", 0, 16, one_level_change, (void*)&img);

	cv::imshow("img", img);
	cv::waitKey();
	return 0;
}

void one_level_change(int pos, void* usrdata)
{
	cv::Mat img = *(cv::Mat*)usrdata;

	img.setTo(pos * 16);
	cv::imshow("img", img);
}