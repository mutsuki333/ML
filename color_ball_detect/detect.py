import cv2 as cv
import numpy as np
import sys
import os
import requests

DEBUG = True
# DEBUG = False

# color detection boundaries in BGR
boundaries = [
    # ('yellow',[0, 130, 130], [150, 255, 255]), #yellow test
    ('yellow',[0, 150, 170], [90, 255, 255]), #yellow
    ('red',[0, 0, 200], [70, 120, 255]), #red test
    ('green',[0, 130, 0], [120, 255, 120]), #blue

    # ([17, 15, 100], [50, 56, 200]), #red
    # ([86, 31, 4], [220, 88, 50]), #blue
    # ([103, 86, 65], [145, 133, 128]) # gray
]

boundaries_H = [
    ('yellow',[0, 150, 170], [90, 255, 255]),
    ('red',[0, 0, 200], [70, 120, 255]),
    ('green',[44, 210, 50], [71, 240, 80]),
]

# edged image
def edged(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (7, 7), 0)
    edged = cv.Canny(gray, 50, 100)
    edged = cv.dilate(edged, None, iterations=2)
    edged = cv.erode(edged, None, iterations=2)
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
    i = -1
    # loop over the boundaries
    for (color, lower, upper) in boundaries:
        i += 1
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
    
        # find the colors within the specified boundaries and apply the mask
        if i == 3:
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            lower = np.array(boundaries_H[2][1], dtype = "uint8")
            upper = np.array(boundaries_H[2][2], dtype = "uint8")
            mask = cv.inRange(hsv, lower, upper)
            output = cv.bitwise_and(hsv, hsv, mask = mask)
            if DEBUG:
                output = cv.cvtColor(output, cv.COLOR_HSV2BGR)
        else:
            mask = cv.inRange(img, lower, upper)
            output = cv.bitwise_and(img, img, mask = mask)


        ## fit shape
        
        #circle
        # c_pic = output.copy()
        # for c,r in fit_circle(c_pic):
        #     print(c,r)
        #     cv.circle(c_pic,c,r,(0,255,0),2)
        
        #ellipse
        if not DEBUG:
            profile[color]={'max':0,'direction':'clear'}
        else:
            profile[color]={'title':color,'fit':[],'max':0,'direction':'clear'}
        e_pic = output.copy()
        e_tmp = []
        fitted = list( fit_ellipse(e_pic) )
        if len(fitted) > 0:
            while len(fitted)>=1:
                i = fitted.index(max(fitted, key=ellipse_size))
                ratio = fitted[i][1][0] / fitted[i][1][1]
                if ratio < 2.2 and ratio > 0.4:
                    e_tmp.append(fitted[i])
                    if DEBUG:
                        profile[color]['fit'].append(fitted[i])
                    size = ellipse_size(fitted[i])
                    if size > profile[color]['max']:
                        profile[color]['max'] = size
                fitted.pop(i)
                if len(e_tmp) >= 2:
                    break

            # determin direction
            if len(e_tmp) == 2:
                center = ( e_tmp[0][0][0]+e_tmp[1][0][0] ) / 2
                shift = center-320
                delta = 10
                if shift > delta:
                    profile[color]['direction']='right'
                elif shift < delta:
                    profile[color]['direction']='left'
            
            if DEBUG:
                for ellipse in e_tmp:
                    cv.ellipse(e_pic,ellipse,(255,0,0),2)

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

    # determine direction


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
            print( main('capture.jpg') )
        except:
            print(main.__doc__)