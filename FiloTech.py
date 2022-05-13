import cv2 as cv
import numpy as np

def emptyFunc(x):
    pass
    #this is an empty function that does nothing, but it's necessary for trackbar.

cap = cv.VideoCapture(0)
width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

kernel = np.ones((5, 5))
#kernel for dilation


#Warning if trackbars fail to work, you can change values by changing default values of bars from below
cv.namedWindow("Parameters")
#cv.resizeWindow("Parameters", 640, 480)
cv.createTrackbar("GaussBlur", "Parameters", 1, 30, emptyFunc)
cv.createTrackbar("CannyThresh1", "Parameters", 24, 255, emptyFunc)
cv.createTrackbar("CannyThresh2", "Parameters", 19, 255, emptyFunc)
cv.createTrackbar("DilationIteration", "Parameters", 1, 20, emptyFunc)
cv.createTrackbar("MinArea", "Parameters", 20000, int(width * height - 200), emptyFunc)
cv.createTrackbar("MaxArea", "Parameters", int(width * height - 200), int(width * height), emptyFunc)
cv.createTrackbar("MinPoints", "Parameters", 7, 30, emptyFunc)
cv.createTrackbar("MaxPoints", "Parameters", 9, 30, emptyFunc)
cv.createTrackbar("PolylineCoefficient", "Parameters", 2, 200, emptyFunc)
#last value will be divided by 100




while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera")
        exit(1)
    #capturing live video frame by frame
    #cv.imshow("frame", frame)
    #uncomment previous line for raw frame

    blurCoefficient = cv.getTrackbarPos("GaussBlur", "Parameters")
    bluredFrame = cv.GaussianBlur(frame, (7, 7), blurCoefficient)
    #cv.imshow("blured frame", bluredFrame)
    #uncomment previous line for blured frame

    grayFrame = cv.cvtColor(bluredFrame, cv.COLOR_BGR2GRAY)
    cv.imshow("gray frame", grayFrame)
    #uncomment previous line for gray frame

    cannyThresh1 = cv.getTrackbarPos("CannyThresh1", "Parameters")
    cannyThresh2 = cv.getTrackbarPos("CannyThresh2", "Parameters")
    cannyFrame = cv.Canny(bluredFrame, cannyThresh1, cannyThresh2)
    #cv.imshow("canny frame", cannyFrame)
    #uncomment previous line for canny edge frame

    numberOfIterations = cv.getTrackbarPos("DilationIteration", "Parameters")
    dilatedFrame = cv.dilate(cannyFrame, kernel, iterations=numberOfIterations)
    cv.imshow("dilated frame", dilatedFrame)
    #uncomment previous line for dilated frame

    #Putting FiloTech Robotics on top of frame
    cv.putText(frame, "FiloTech Robotics", (50, 50), cv.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 255), 2)

    #getting contours from frame
    contours, hierarchy = cv.findContours(dilatedFrame, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    #different types of retrieving methods can be used later
    for contour in contours:
        contourArea = cv.contourArea(contour)
        minimumContourArea = cv.getTrackbarPos("MinArea", "Parameters")
        maximumContourArea = cv.getTrackbarPos("MaxArea", "Parameters")
        if maximumContourArea > contourArea > minimumContourArea:
            cv.drawContours(frame, contour, -1, (255, 0, 0), 5)
            coefficient = cv.getTrackbarPos("PolylineCoefficient", "Parameters") / 100
            approx = cv.approxPolyDP(contour, coefficient * cv.arcLength(contour, True), True)
            minimumPoints = cv.getTrackbarPos("MinPoints", "Parameters")
            maximumPoints = cv.getTrackbarPos("MaxPoints", "Parameters")
            if maximumPoints > len(approx) > minimumPoints:
                x, y, w, h = cv.boundingRect(approx)
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
                cv.putText(frame, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)
                cv.putText(frame, "Area: " + str(int(contourArea)), (x + w + 20, y + 45), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
    cv.imshow("Final Frame", frame)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break