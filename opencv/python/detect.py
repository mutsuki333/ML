import cv2 as cv
import numpy as np
import sys
import os
import requests

DEBUG = True

# color detection boundaries in BGR
boundaries = [
    ('yellow',[0, 130, 130], [150, 255, 255]), #yellow test
    # ('yellow',[25, 146, 190], [62, 174, 250]), #yellow
    ('red',[0, 0, 80], [50, 56, 200]), #red test
    ('green',[0, 80, 0], [56, 200, 50]), #blue

    # ([17, 15, 100], [50, 56, 200]), #red
    # ([86, 31, 4], [220, 88, 50]), #blue
    # ([103, 86, 65], [145, 133, 128]) # gray
]

# edged image
def edged(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (7, 7), 0)
    edged = cv.Canny(gray, 50, 100)
    edged = cv.dilate(edged, None, iterations=1)
    edged = cv.erode(edged, None, iterations=1)
    return edged

def fit_ellipse(image):
    contours, hierarchy = cv.findContours(edged(image), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if len(cnt)<5: continue
        yield(cv.fitEllipse(cnt))

def fit_circle(image):
    contours, hierarchy = cv.findContours(edged(image), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        (x,y),radius = cv.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        yield(center,radius)

def ellipse_size(item):
    return max([item[1][0],item[1][1]])

def main(file_path):
    """
    Usage: python detect.py PATH/TO/FILE
    """
    profile={}

    DIR = os.path.dirname(os.getcwd())
    img = cv.imread(file_path,cv.IMREAD_COLOR)
    if DEBUG: print('image size : {}'.format(img.shape))

    # color detect
    result = None
    # loop over the boundaries
    for (color, lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
    
        # find the colors within the specified boundaries and apply the mask
        mask = cv.inRange(img, lower, upper)
        output = cv.bitwise_and(img, img, mask = mask)
        # output = cv.bitwise_xor(img, output)

        ## fit shape
        
        #circle
        # c_pic = output.copy()
        # for c,r in fit_circle(c_pic):
        #     print(c,r)
        #     cv.circle(c_pic,c,r,(0,255,0),2)
        
        #ellipse
        profile[color]={'title':color,'fit':[]}
        e_pic = output.copy()
        e_tmp = []
        fitted = list( fit_ellipse(e_pic) )
        if len(fitted) >= 2:
            # 1st max
            i = fitted.index(max(fitted, key=ellipse_size))
            e_tmp.append(fitted[i])
            fitted.pop(i)
            # 2nd max
            i = fitted.index(max(fitted, key=ellipse_size))
            e_tmp.append(fitted[i])
            fitted.pop(i)

            for ellipse in e_tmp:
                if DEBUG:
                    cv.ellipse(e_pic,ellipse,(255,0,0),2)
                profile[color]['fit'].append(ellipse)

        # print results in debug mode
        if DEBUG:
            if __name__ == '__main__':
                display = np.hstack([img, output, e_pic])
                if result is not None:
                    result = np.vstack([result, display])
                else:
                    result = display
            else:
                cv.imwrite('uploads/{}.png'.format(color),e_pic)


    # display
    if DEBUG and __name__ == '__main__':
        print(profile)
        result = cv.resize(result,(960,720))
        cv.imshow("images", result)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    else: return profile
    
if __name__ == '__main__':
    
    try:
        print(main(sys.argv[1]))
    except IndexError:
        try:
            url = 'http://192.168.1.26/'
            r = requests.get(url, allow_redirects=True)
            open('capture.jpg', 'wb').write(r.content)
            main('capture.jpg')
        except:
            print(main.__doc__)