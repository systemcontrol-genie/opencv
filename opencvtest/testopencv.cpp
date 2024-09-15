#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main() {
    // 이미지 파일을 읽어옵니다.
    Mat image = imread("test.png");

    // 이미지가 제대로 로드되지 않은 경우, 오류 메시지를 출력합니다.
    if (image.empty()) {
        cout << "Image not found or unable to open!" << endl;
        return -1;
    }

    // 이미지 창을 생성하고 이미지를 표시합니다.
    namedWindow("image", WINDOW_AUTOSIZE);
    imshow("image", image);

    // 키 입력을 기다립니다.
    waitKey(0);

    // 모든 창을 닫습니다.
    destroyAllWindows();

    return 0;
}
