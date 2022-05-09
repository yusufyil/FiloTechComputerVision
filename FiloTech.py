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

cv.namedWindow("Parameters")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera")
        exit(1)
    #capturing live video frame by frame
    cv.imshow("frame", frame)
    #uncomment previous line for raw frame

    bluredFrame = cv.GaussianBlur(frame, (7, 7), 1)
    cv.imshow("blured frame", bluredFrame)
    #uncomment previous line for blured frame

    grayFrame = cv.cvtColor(bluredFrame, cv.COLOR_BGR2GRAY)
    cv.imshow("gray frame", grayFrame)
    #uncomment previous line for gray frame

    cannyFrame = cv.Canny(bluredFrame, 20, 23)
    cv.imshow("canny frame", cannyFrame)
    #uncomment previous line for canny edge frame

    dilatedFrame = cv.dilate(cannyFrame, kernel, iterations=1)
    cv.imshow("dilated frame", dilatedFrame)
    #uncomment previous line for dilated frame
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break