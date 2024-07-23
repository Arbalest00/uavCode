import cv2
import numpy as np
RED_UPPER = np.array([10, 255, 255])
RED_LOWER = np.array([0, 43, 46])
RED_UPPER2 = np.array([180, 255, 255])
RED_LOWER2 = np.array([156, 43, 46])
RED_UPPERF = np.array([180, 255, 255])
RED_LOWERF = np.array([150, 120, 120])
def red_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    """ mask1 = cv2.inRange(hsv, RED_LOWER, RED_UPPER)
    mask2 = cv2.inRange(hsv, RED_LOWER2, RED_UPPER2)
    res = mask1 + mask2 """
    mask=cv2.inRange(hsv,RED_LOWERF,RED_UPPERF)
    res=mask
    return res
if __name__ == '__main__':
    cap=cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640.0)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480.0)
    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    while cap.isOpened():
        ret, img = cap.read()
        red_img=red_mask(img)
        cv2.imshow('img', img)
        cv2.imshow('red_img', red_img)
        cv2.waitKey(20)
