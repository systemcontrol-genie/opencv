#include <iostream>
#include<opencv2/opencv.hpp>

using namespace std;
using namespace cv;

int main()
{
	Mat image;
	image = imread("C:/Users/lim/Downloads/OIP.jpg");

	if (image.empty())
	{
		cerr << "load image Failed" << endl;
		return -1;
	}
	namedWindow("image");
	imshow("image", image);

	waitKey();
	return 0;
}