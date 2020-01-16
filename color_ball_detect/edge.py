import cv2
import numpy as np
import sys
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt



def edge():
    """
    Usage: python edge.py PATH/TO/FILE
    """

    img = cv2.imread(sys.argv[1],cv2.IMREAD_COLOR)
    edges = cv2.Canny(img,100,200)

    # cv2.imshow('title',edges)
    # cv2.waitKey(0)

    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()

if __name__ == '__main__':
    try:
        edge()
    except IndexError:
        print(edge.__doc__)
        