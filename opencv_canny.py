import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 50,100)
    cv2.imshow("frame", frame)
    cv2.imshow("canny",canny)

    if cv2.waitKey(10) == 27:
        break
cap.release()
cv2.destroyAllWindows()