import cv2 as cv
import numpy as np
import sys, math
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

class structure:
    def __init__(self):
        self.size=0  #length of edge
        self.edge=[]  # [ [x1,y1], [x2,y2], ... ]
        self.edge_gradient=[]

class Structs :
    """
    returns an object of structured edges
    """
    colors = [ #bgr
        [0,0,255], #red
        [0,128,255], #orange
        [0,255,255], #yellow
        [0,128,255],
        [0,255,0],
        [128,255,0],
        [255,255,0],
        [255,128,0],
        [255,0,0],
        [255,0,128],
        [255,0,255]
    ]
    def __init__(self,edged, tolerance=5, minLength=False): 
        """
        This is a class to grasp out structured edges,
            edged: an canny edged img
            tolerance: the tolerance for assuming saperated edges as the same structure
            minLength: the minimum length a structure must be. 
                        Integers for actual number (default 5). or True for relative length to img size.
        """
        self._img = edged.copy()
        self.img = edged.copy()
        self.S=[] # array of structured edges
        if type(tolerance)is not int and tolerance<0:
            tolerance=5
            print('tolerance must be an integer')

        if type(minLength) is bool and minLength:
            minLength = int(self._img.shape[0]/5)
        elif minLength: minLength = int(minLength)
        else : minLength = 5 

        print(self._img.shape)
        self.Ix = self._img.shape[0]
        self.Iy = self._img.shape[1]
        # print(f'minL: {minLength}')

        for x in range(0,self.Ix):
            for y in range(0,self.Iy):
                if self._img.item(x,y) == 0 : continue
                tmp = structure()
                self._edge_search(tmp,x,y,tolerance)
                if tmp.size >= minLength: 
                    self.S.append(tmp)

        # print(sorted(self.S[10].edge,key = lambda x : (x[0], x[1])))
        print(len(self.S))

    def _edge_search(self,e,x,y,tolerance): # e for the edge object
        stack = [[x,y]]
        while stack:
            x, y = stack.pop()
            for tx in range(x-tolerance,x+tolerance):
                if tx < 0: continue
                if tx >= self.Ix : break
                for ty in range(y-tolerance,y+tolerance):
                    if ty < 0: continue
                    if ty >= self.Iy : break
                    if self._img.item(tx,ty)!=0:
                        stack.append([tx,ty])
                        self._img.itemset(tx,ty,0)
                        e.edge.append([tx,ty])
                        e.size += 1
                        self._edge_connect(e,x,y,tx,ty)
                    
    def _edge_connect(self,e,x,y,tx,ty):
        if x == tx or y == ty: return
        for i in np.arange(x+1,tx-1,float(tx-x)/(ty-y)):
            for j in np.arange(y+1,ty-1,float(ty-y)/(tx-x)):
                e.size += 1
                e.edge.append([int(round(i).item()) ,int(round(j).item())])


    def preview(self,img,bold=True): # give a new img to draw on
        img = np.zeros((self.Ix,self.Iy,3), np.uint8)
        c = 0
        for S in self.S:
            for p in S.edge:
                for i in range(0,3):
                    if bold and img.shape[0]>512:
                        w = int(img.shape[0]/256)
                        for bx in range(p[0], p[0]+w):
                            if bx >= img.shape[0] : break
                            for by in range(p[1], p[1]+w):
                                if by >= img.shape[1] : break
                                img.itemset(bx,by,i,self.colors[c][i])

                    else:
                        img.itemset(p[0],p[1],i,self.colors[c][i])
            c+=1
            if c > 10: c=0

        return img

# referenced from web
def get_x_y_c(p,r):
    r = int(round(r))
    x = r-1
    y = 0
    dx = 1
    dy = 1
    err = dx - (r << 1)
    arr = []
    while x >= y :
        arr.append( [p[0] + x, p[1] + y] )
        arr.append( [p[0] + y, p[1] + x] )
        arr.append( [p[0] - y, p[1] + x] )
        arr.append( [p[0] - x, p[1] + y] )
        arr.append( [p[0] - x, p[1] - y] )
        arr.append( [p[0] - y, p[1] - x] )
        arr.append( [p[0] + y, p[1] - x] )
        arr.append( [p[0] + x, p[1] - y] )
        if err <= 0 :
            y+=1
            err += dy
            dy += 2
        if err > 0:
            x-=1
            dx += 2
            err += dx - (r << 1)

    return np.array(arr).astype(int)

def _close_with_err(p1,p2,err=10):
    if abs(p1[0]-p2[0]) <= err and abs(p1[1]-p2[1]) <= err:
        return True
    else: return False

def circles(struct, tolerance=5, minR=20, maxTry=50, fit=1/3):
    """
    Usage: circles(cv::img_edged) : [x,y,radius]
    """
    maxTry *= 3
    if len(struct.S) < 20: maxTry *= 100
    circle = [] # [  [x,y,r,fit], ....  ]
    # np.random.seed(int(time.time()))
    for s in struct.S:
        base = 0
        # s = struct.S[8]
        e = np.array(s.edge)
        # print(len(e))
        np.random.shuffle( e )
        while base+2 < s.size and base<maxTry:
            p1, p2, p3 = e[base], e[base+1], e[base+2]
            base +=3 
            
            # referenced from web
            # 三點找圓 
            temp = p2[0] * p2[0] + p2[1] * p2[1]
            bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
            cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
            det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

            if abs(det) < 1.0e-6: continue

            # Center of circle
            cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
            cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det
            radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
            # print(f'r: {radius}, minR: {minR}')
            if radius < minR: continue

            pts = get_x_y_c([cx,cy],radius) 
            ctr = 0
            for pt in pts:
                if pt[0] >= struct.img.shape[0] or pt[0]<0 or pt[1] < 0 or pt[1] >= struct.img.shape[1] :
                    continue
                if struct.img.item(pt[0],pt[1]) != 0:
                    ctr += 1
            cfit = float(ctr/len(pts))

            # if cx > 0 and cx < 1000 and cy > 0 and cy < 1000:
            #     circle.append([cx,cy,radius,cfit])

            if cfit >= fit:
                duplicated_at = -1
                for indx, c in enumerate(circle):
                    if _close_with_err([cx,cy],[c[0],c[1]],tolerance)  and abs(radius-c[2])<=tolerance: # 確認是否有一樣的圓
                        if duplicated_at == -1: duplicated_at = -2  # If the same circle was found, and this one is not better. 
                        if cfit > c[3]: #確認一樣的圓是否有更好
                            duplicated_at = indx

                if duplicated_at == -1:
                    circle.append([cx,cy,radius,cfit])
                elif duplicated_at >= 0:
                    circle[duplicated_at] = [cx,cy,radius,cfit]
        # break

    print(np.array(circle))
    if len(circle) <=0 : return None
    else : return circle

def main():
    """
    Usage: python d&c.py PATH/TO/FILE
    """

    img = cv.imread(sys.argv[1],cv.IMREAD_COLOR)
    # img = cv.resize(img,(int(img.shape[1]/4),int(img.shape[0]/4)),interpolation=cv.INTER_AREA)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    edged = cv.Canny(gray, 35, 125, L2gradient = True)

    # edged = cv.resize(edged,(int(img.shape[1]/4),int(img.shape[0]/4)),interpolation=cv.INTER_AREA)


    S = Structs(edged)

    circle = circles(S,minR=img.shape[0]/50, fit=0.5)

    # img = cv.resize(img,(int(img.shape[1]/4),int(img.shape[0]/4)),interpolation=cv.INTER_AREA)
    img2 = img.copy()
    # circle = None
    if circle is not None : print(f'Number of circles: {len(circle)}')
    else : print('No circles found.')


    if circle is not None:
        circle = np.uint16(np.around(circle))
        for i in circle:
            center = (i[0], i[1])
            # circle center
            cv.circle(img2, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(img2, center, radius, (255, 0, 255), 2)
    

    grid = plt.GridSpec(2, 3)
    # plt.figure(figsize=(10,5))
    plt.subplot(grid[0,0]),plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])

    plt.subplot(grid[0,1]),plt.imshow(cv.cvtColor(gray, cv.COLOR_BGR2RGB))
    plt.title('Gray Image'), plt.xticks([]), plt.yticks([])

    plt.subplot(grid[0,2]),plt.imshow(cv.cvtColor(edged, cv.COLOR_BGR2RGB))
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.subplot(grid[1,0]),plt.imshow(cv.cvtColor(S.preview(img), cv.COLOR_BGR2RGB))
    plt.title('Structured edges'), plt.xticks([]), plt.yticks([])

    plt.subplot(grid[1,1]),plt.imshow(cv.cvtColor(img2, cv.COLOR_BGR2RGB))
    plt.title('Circle Image'), plt.xticks([]), plt.yticks([])

    # img3 = cv.resize(img,(int(img.shape[1]/10),int(img.shape[0]/10)),interpolation=cv.INTER_CUBIC)
    # plt.subplot(grid[1,2]),plt.imshow(cv.cvtColor(img3, cv.COLOR_BGR2RGB))
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()

if __name__ == '__main__':
    try:
        sys.argv[1]
    except IndexError:
        print(main.__doc__)
    else:
        main()
        