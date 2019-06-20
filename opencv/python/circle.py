import cv2 as cv
import numpy as np
import sys
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt



def circle():
    """
    Usage: python circle.py PATH/TO/FILE
    """

    img = cv.imread(sys.argv[1],cv.IMREAD_COLOR)
    img2 = img.copy()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.Canny(gray,100,200)
    # gray = cv.medianBlur(gray, 5)

    # cv.imshow('title',gray)
    # cv.waitKey(0)
    # return

    # circles = cv.HoughCircles(gray,cv.HOUGH_GRADIENT,1,20,
    #                         param1=100,param2=20,minRadius=100,maxRadius=200)

    circles = cv.HoughCircles(gray,cv.HOUGH_GRADIENT,1,20,
                            param1=50,param2=39.5,minRadius=0,maxRadius=0)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            print(i)
            center = (i[0], i[1])
            # circle center
            cv.circle(img2, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(img2, center, radius, (255, 0, 255), 3)
    

    cv.imshow('title',np.hstack([img, cv.cvtColor(gray, cv.COLOR_GRAY2BGR), img2]))
    # cv.imshow('title',gray)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # plt.subplot(121),plt.imshow(img,cmap = 'gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    # plt.show()

if __name__ == '__main__':
    try:
        circle()
    except IndexError:
        print(circle.__doc__)
        