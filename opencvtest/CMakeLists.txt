cmake_minimum_required(VERSION 3.30)  # 올바른 입력

project(opencvtest)
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
add_executable(opencvtest testopencv.cpp)
target_link_libraries(opencvtest ${OpenCV_LIBS})