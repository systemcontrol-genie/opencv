import cv2

img_rgb = cv2.imread("C:/Users/user/Desktop/OIP.jpg", cv2.IMREAD_COLOR) #color 로 이미지 출력
img_gray = cv2.imread("C:/Users/user/Desktop/OIP.jpg", cv2.IMREAD_GRAYSCALE) # gray이미지로 출력위해서 
#img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
img_alpa = cv2.imread("C:/Users/user/Desktop/OIP.jpg", cv2.IMREAD_UNCHANGED)

print(img_rgb.shape)

cv2.imshow("RGB",img_rgb)
cv2.imshow("gray",img_gray)
cv2.imshow("alpa", img_alpa)
cv2.imwrite("C:/Users/user/Documents/KAIROS/image/test.png", img_gray)
cv2.waitKey()
cv2.destroyAllWindows()
