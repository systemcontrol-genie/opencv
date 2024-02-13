import cv2
import numpy as np


def detect_white_yellow(image):
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for white color
    lower_white = np.array([0, 0, 200], dtype=np.uint8)
    upper_white = np.array([180, 30, 255], dtype=np.uint8)

    # Define lower and upper bounds for yellow color
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

    # Create masks for white and yellow colors
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Combine masks
    mask = cv2.bitwise_or(mask_white, mask_yellow)

    # Apply mask to original image
    result = cv2.bitwise_and(image, image, mask=mask)

    return result

def gray_image(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img , low_threshold, high_threshold)

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)

    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,)*channel_count
    else:
        ignore_mask_color = 255
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_line(img, lines, color=[0,255,0], thickness=3):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1 ,y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_line(line_img, lines)
    return line_img

def weighted_img(lines, img, alpha=0.8, beta=1):
    return cv2.addWeighted(lines, alpha, img, beta, 0)


cap = cv2.VideoCapture('C:/Users/lim/Downloads/videoplayback (1).mp4')

while True:
   ret, frame = cap.read()

   if not ret:
       cap.release()
       break
   wy = detect_white_yellow(frame)
   gray_frame = gray_image(frame)
   gaussian_frame = gaussian_blur(gray_frame, 5)
   canny_frame = canny(gaussian_frame, 120, 200)
   imshape = frame.shape  # ROI region
   #vertices = np.array([[(150, imshape[0]), (550, 450), (750, 450), (imshape[1], imshape[0])]], dtype=np.int32)
   vertices = np.array([[(160, imshape[0]), (540, 410), (600, 410), (280, imshape[0])]], dtype=np.int32)
   vertices1 = np.array([[(imshape[1]-400, imshape[0]), (640, 410), (700, 410), (imshape[1]-250, imshape[0])]], dtype=np.int32)
   mask1 = region_of_interest(canny_frame, vertices)
   mask2 = region_of_interest(canny_frame, vertices1)
   merged_mask = cv2.bitwise_or(mask1, mask2)
   lines = hough_lines(merged_mask, 2, np.pi/180, 90, 120, 150)
   lines_edges = weighted_img(lines, frame, alpha=0.8, beta=1.)
   cv2.imshow("Video", lines_edges)

   if cv2.waitKey(10) == 27:
       cap.read()
       break

cv2.destroyAllWindows()
