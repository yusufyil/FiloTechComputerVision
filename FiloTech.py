import math
import time

import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
print(width, "   ", height)

kernel = np.ones((5, 5))


class ResultSet:
    def __init__(self, numberOfFrames):
        self.numberOfFrames = numberOfFrames
        self.index = 0
        self.storage = [[0, 0, 0, 0] for i in range(self.numberOfFrames)]
        self.average_result = []

    def insert(self, bounding_box):
        self.storage[self.index] = bounding_box
        self.index = (self.index + 1) % self.numberOfFrames

    def calculateAverage(self, list=[], order=0):
        summation = 0
        number_0f_zeroes = 0
        for i in range(self.numberOfFrames):
            summation += self.storage[i][order]
            if self.storage[i][3] == 0:
                number_0f_zeroes += 1
        if number_0f_zeroes >= self.numberOfFrames // 2:
            return 0
        else:
            return summation // (self.numberOfFrames - number_0f_zeroes)

    def getAverage(self):
        averageX = self.calculateAverage(self.storage, 0)
        averageY = self.calculateAverage(self.storage, 1)
        averageW = self.calculateAverage(self.storage, 2)
        averageH = self.calculateAverage(self.storage, 3)
        return [averageX, averageY, averageW, averageH]


# kernel for dilation

def filterImage(video_frame):
    cv.imshow("frame", video_frame)

    bluredFrame = cv.GaussianBlur(frame, (5, 5), 0)
    # cv.imshow("blured frame", bluredFrame)

    grayFrame = cv.cvtColor(bluredFrame, cv.COLOR_BGR2GRAY)
    cv.imshow("gray frame", grayFrame)
    # uncomment previous line for gray frame

    cannyFrame = cv.Canny(bluredFrame, 100, 255)
    # cv.imshow("canny frame", cannyFrame)

    dilatedFrame = cv.dilate(cannyFrame, kernel, iterations=1)
    cv.imshow("dilated frame", dilatedFrame)
    # uncomment previous line for dilated frame

    return dilatedFrame


rs = ResultSet(10)

while True:

    inserted = False

    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera")
        exit(1)
    # capturing live video frame by frame
    cv.imshow("frame", frame)

    filtered_frame = filterImage(frame)

    # Putting FiloTech Robotics on top of frame
    cv.putText(frame, "FiloTech Robotics", (50, 50), cv.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 255), 2)

    # getting contours from frame
    contours, hierarchy = cv.findContours(filtered_frame, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    # different types of retrieving methods can be used later

    for contour in contours:
        contourArea = cv.contourArea(contour)
        if int(width * height - 200) > contourArea > 20000:
            cv.drawContours(frame, contour, -1, (255, 0, 0), 5)
            approx = cv.approxPolyDP(contour, 0.02 * cv.arcLength(contour, True), True)
            if 9 > len(approx) > 7:
                x, y, w, h = cv.boundingRect(approx)
                rs.insert([x, y, w, h])
                inserted = True
    if not inserted:
        rs.insert([0, 0, 0, 0])

    box = rs.getAverage()
    if box[3] != 0:
        cv.rectangle(frame, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 0, 255), 5)
    # rest of the code will maneuver robot
    if box[2] == 0 or box[3] == 0:
        print("Looking for circle..")
    else:
        center_of_circle_x = box[0] + box[2] // 2
        center_of_circle_y = box[1] + box[3] // 2
        print("Center coordinates of circle: ", center_of_circle_x, center_of_circle_y)
        print("Angle of circle towards robot's front",
              math.acos(box[3] / math.sqrt((math.pow(box[2], 2) + math.pow(box[3], 2)))))
        if width // 2 + (width // 10) > center_of_circle_x > width // 2 - (width // 10):
            print("Go ahead! ^^^^^^^^^^^^^")
        elif center_of_circle_x > width // 2 + (width // 10):
            print("Turn right! >>>>>>>>>>>>")
        elif center_of_circle_x < width // 2 - (width // 10):
            print("Turn left! <<<<<<<<<<<<")

    cv.imshow("Final Frame", frame)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break

