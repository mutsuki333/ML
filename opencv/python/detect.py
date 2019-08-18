import cv2 as cv
import numpy as np
import sys
import os

# Debug
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

def main(file_path):
    """
    Usage: python detect.py PATH/TO/FILE
    """
    img = cv.imread(file_path,cv.IMREAD_COLOR)
    img2 = img.copy()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.Canny(gray,100,200)

    # gray = cv.GaussianBlur(gray, (5, 5), 0)


    # display
    DIR = os.path.dirname(os.getcwd())
    if __name__ == '__main__':
        cv.imshow('title',gray)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        cv.imwrite('{}/uploads/gray.png'.format(DIR),gray)


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print(main.__doc__)