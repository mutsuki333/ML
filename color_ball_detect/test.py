import cv2 as cv
import numpy as np
import sys
import os

def main(image=None):
    """
    Usage: python detect.py PATH/TO/FILE
    """
    image = image or cv.imread('uploads/red.png',cv.IMREAD_COLOR)

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (7, 7), 0)

    edged = cv.Canny(gray, 50, 100)
    edged = cv.dilate(edged, None, iterations=1)
    edged = cv.erode(edged, None, iterations=1)

    contours, hierarchy = cv.findContours(edged.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        #ellipse
        ellipse = cv.fitEllipse(cnt)
        print(ellipse)
        cv.ellipse(image,ellipse,(255,0,0),2)

        # rect
        # rect = cv.minAreaRect(cnt)
        # box = cv.boxPoints(rect)
        # box = np.int0(box)
        # cv.drawContours(image,[box],0,(0,255,0),2)
        # print('rect : {}'.format())

    cv.imshow("result", image)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except IndexError:
        print("err")