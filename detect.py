import cv2
ss = cv2.CascadeClassifier("stopsign_classifier.xml")
cap = cv2.VideoCapture(0)
cap.set(16,640)
cap.set(9,360)
count = 0
while True:
    ret,img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Screen", img)
    S = ss.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,x) in S:
        count = count + 1
        print("Stop Sign Detected ", count)

    key = cv2.waitKey(30)
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break