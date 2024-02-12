#include <iostream>
#include <opencv2/opencv.hpp>

void main()
{
	cv::VideoCapture cap(0);

	if (!cap.isOpened())
	{
		std::cerr << "Camera open failed! \n" << std::endl;
		return;
	}
	std::cout << "frame witdh :" << cvRound(cap.get(cv::CAP_PROP_FRAME_WIDTH))<< std::endl;
	std::cout << "frame Height:" << cvRound(cap.get(cv::CAP_PROP_FRAME_HEIGHT)) << std::endl;

	cv::Mat frame, inversed;
	while (true)
	{
		cap >> frame;
		if (frame.empty())
			break;

		inversed = ~frame;

		cv::imshow("frame", frame);
		cv::imshow("inversed", inversed);

		if (cv::waitKey(10) == 27)
			break;
	}
	cv::destroyAllWindows();
}