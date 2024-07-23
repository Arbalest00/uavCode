import cv2
import numpy as np
# from Lpid import PID3
import time

debug = False
arr = []
filt_cnt = 3
filt_dis = 9000
area_min = 0
area_max = 10000
def find_largest_contour_center(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(max_contour)
        if(debug == True):
            pass
            #print(area)
        if area_max > area > area_min:  # 添加判断条件，只返回面积大于area的轮廓中点坐标
            M = cv2.moments(max_contour)
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])
            cv2.drawContours(image, [max_contour], -1, (0, 255, 0), 2)
            return image, center_x, center_y
    return image, None, None

def find_laser_point(img):
    frame = img
    h_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 20, 210])
    upper_red = np.array([50, 255, 240])
    mask = cv2.inRange(h_img, lower_red, upper_red)
    res = cv2.bitwise_and(img, h_img, mask=mask)
    kernel = np.ones((9, 9), np.uint8)
    res = cv2.dilate(res, kernel)
    kernel = np.ones((3, 3), np.uint8)
    res = cv2.erode(res, kernel)
    kernel = np.ones((9, 9), np.uint8)
    res = cv2.dilate(res, kernel)
    kernel = np.ones((3, 3), np.uint8)
    res = cv2.erode(res, kernel)
    res = find_largest_contour_center(res)
    img_res = res[0]
    loc = [res[1], res[2]]
    if(debug == True):
        cv2.imshow('res', img_res)
    return img_res, loc

def get_fire_loc(img):
    img_res, loc = find_laser_point(img)
    if loc[0] is not None and loc[1] is not None:
        if(len(arr) <5):
            arr.append(loc)
        elif(len(arr)==5):
            cnt = 0
            for i in range(5):
                dis = (loc[0] - arr[i][0])**2 + (loc[1] - arr[i][1])**2
                if(dis <= filt_dis):
                    cnt += 1
            arr.append(loc)
            arr.pop(0)
            if(cnt >= filt_cnt):
                return loc
    else:
        return None


if __name__ == "__main__":
#     x_pid=PID3(0,240)
#     y_pid=PID3(0,320)
    debug=True
    cam=cv2.VideoCapture(0)
    while cam.isOpened():
        ret, img = cam.read()
        cv2.imshow('img', img)
        res = get_fire_loc(img)
        if(res != None):
#             x_speed=x_pid.get_pid(res[1])
#             y_speed=y_pid.get_pid(res[0])
            print(res)
#             print(x_speed)
#             print(y_speed)
        cv2.waitKey(20)
