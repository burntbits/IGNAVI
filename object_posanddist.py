import numpy as np 
import cv2 as cv
import time
import ftpfetch as ft
output = open ("output.txt", "w")
STEP_DIST = 40
def findStuff():
    depth_img = cv.imread ("depth_out.png")
    gray_out = cv.cvtColor(depth_img, cv.COLOR_BGR2GRAY)
    ret,thresh = cv.threshold(gray_out,237,255,cv.THRESH_BINARY)
    kernel = np.ones((5,5),np.uint8)
    thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
    thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(gray_out, contours, -1, (0,255,0), 3)
    count=0
    for i in contours:
        M = cv.moments(i)
        if M['m00'] != 0:
            dist = cv.pointPolygonTest((contours[count]), (320,240), True)
            count = count + 1
            test = ("Object ",str(count), " at ")
            output.write (''.join(test))
            if (dist > 15):
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                if (cx >= 360):
                    test = ("approximately ",str(round(abs(dist)/STEP_DIST, 2)), " steps right\n",)
                    output.write (''.join(test))
                elif (cx <=280):
                    test ("approximately ", str(round(abs(dist)/STEP_DIST, 2)), " steps left\n")
                    output.write (''.join(test))
                else:
                   test = ("center\n")
                   output.write (''.join(test))
            else:
                test = ("center\n")
                output.write (''.join(test))
    cv.imwrite('image.png', gray_out)
    ft.ftp_send()
if __name__ == '__main__':
    findStuff()