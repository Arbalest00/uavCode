import cv2
import numpy as np
from collections import defaultdict
import time


class radar_cv:
    res_cache = []

    def __init__(self) -> None:
        pass

    def extract_white(self, image):
        # image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        mask = np.zeros_like(image)
        # 将二值图像中的白色部分复制到掩膜图像中
        mask[binary == 255] = image[binary == 255]
        return mask

    def dilate_erode(self, image):
        # 膨胀
        kernel_dilate = np.ones((7, 7), np.uint8)
        # 腐蚀
        kernel_erode = np.ones((3, 3), np.uint8)
        dilated_image = cv2.dilate(image, kernel_dilate, iterations=2)
        eroded_image = cv2.erode(dilated_image, kernel_erode, iterations=1)
        return eroded_image

    def dilate_erode_res(self, image):
        kernel_dilate = np.ones((3, 3), np.uint8)
        kernel_erode = np.ones((30, 30), np.uint8)
        dilated_image = cv2.dilate(image, kernel_dilate, iterations=2)
        eroded_image = cv2.erode(dilated_image, kernel_erode, iterations=1)
        return eroded_image

    def dilate_erode_circle(self, image):
        kernel_dilate = np.ones((3, 3), np.uint8)
        kernel_erode = np.ones((2, 2), np.uint8)
        dilated_image = cv2.dilate(image, kernel_dilate, iterations=2)
        eroded_image = cv2.erode(dilated_image, kernel_erode, iterations=1)
        return eroded_image

    def remove_lines(self, image):
        # 将图像转换为灰度图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 使用Canny边缘检测算法进行边缘检测
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        # 运行Hough直线变换检测直线
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=30)
        mask = np.zeros_like(image)
        # 在掩膜图像上绘制检测到的直线
        try:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(mask, (x1, y1), (x2, y2), (255, 255, 255), 100)
            # 将直线从原始图像中去除
            result = cv2.subtract(image, mask)
        except:
            result = image
        return result

    def blacken_edges(self, image):
        height, width = image.shape[:2]
        edge_length = min(height, width) // 8
        result = np.copy(image)
        # 将边缘边长1/8的部分全部变成黑色
        result[:edge_length, :] = (0, 0, 0)
        result[-edge_length:, :] = (0, 0, 0)
        result[:, :edge_length] = (0, 0, 0)
        result[:, -edge_length:] = (0, 0, 0)
        return result

    def draw_res(self, image, size):
        height, width = image.shape[:2]
        region_width = width // size
        region_height = height // size
        result = np.zeros_like(image)
        # 遍历每个区域
        for i in range(size):
            for j in range(size):
                # 计算当前区域的横坐标范围和纵坐标范围
                x_start = i * region_width
                x_end = (i + 1) * region_width
                y_start = j * region_height
                y_end = (j + 1) * region_height
                # 在当前区域内查找白点
                white_points = np.where(
                    image[y_start:y_end, x_start:x_end] == 255)
                # 如果有白点，则计算白点的平均坐标
                if len(white_points[0]) > 0:
                    x_avg = int(np.mean(white_points[1]) + x_start)
                    y_avg = int(np.mean(white_points[0]) + y_start)
                    cv2.circle(result, (x_avg, y_avg), 3, (255, 255, 255), -1)
        return result

    def detect_circles(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 对灰度图进行模糊处理，以减少噪声对霍夫圆检测的影响
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # 进行霍夫圆检测
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1,
                                   minDist=50, param1=50, param2=10, minRadius=1, maxRadius=10)
        # 如果没有检测到圆，则返回空列表
        if circles is None:
            return []
        # 将检测到的圆的坐标转换为整数
        circles = np.round(circles[0, :]).astype("int")
        # 在图像上标出检测到的圆
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(image, (x - r - 10, y - r - 10),
                          (x + r + 10, y + r + 10), (0, 128, 255), 2)
            # 在图像上显示文本
            text = str([x, y])
            org = (x - r - 10, y - r - 30)  # 文本的起始坐标
            fontFace = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 0.4
            color = (0, 255, 0)  # 文本颜色为绿色
            thickness = 1
            # 在图像上绘制文本
            cv2.putText(image, text, org, fontFace,
                        fontScale, color, thickness)
        return [circles, image]

    def show_test_res(self, image):
        # image_path = "radar_map.jpg"
        # res_cir = None
        res = self.extract_white(image)
        # res_0 = res
        res = self.dilate_erode(res)
        res = self.remove_lines(res)
        res = self.blacken_edges(res)
        res = self.dilate_erode(res)
        res = self.dilate_erode(res)
        res = self.dilate_erode_res(res)
        # res_1 = res
        res = self.draw_res(res, 20)
        res = self.dilate_erode_circle(res)
        try:
            res_tmp = self.detect_circles(res)[0]
            try:
                res_cir_edit = []
                for i in range(len(res_tmp)):
                    res_cir_x = int(res_tmp[i][0])
                    res_cir_y = int(res_tmp[i][1])
                    res_cir = [res_cir_x, res_cir_y]
                    res_cir_edit.append(res_cir)
                    # res = res_tmp[1]
                    # print(res_cir)
                    # self.res_cache.append(res_cir)
                # print(res_cir_edit)
                # self.res_cache.append(res_cir_edit)
            except:
                res_cir_edit = []
                pass
            self.res_cache.append(res_cir_edit)
        except:
             res_cir_edit = []
        return res_cir_edit

    def filt(self, img):
        # img = cv2.imread('radar_map.jpg')
        arr = self.show_test_res(img)
        # print(arr)
        len_cache = len(self.res_cache)
        if (len_cache >= 5):
            arr_tmp = self.res_cache[len_cache-5:len_cache]
            # print(arr_tmp)
            flattened_arr = []
            for i in range(len(arr_tmp)):
                for j in range(len(arr_tmp[i])):
                    flattened_arr.append(arr_tmp[i][j])
            # arr = arr_tmp
            arr = flattened_arr
            # print(arr)
            point_counts = defaultdict(int)
            merged_points = []
            for i in range(len(arr)):
                x, y = arr[i]
                merged = False
                if i > 0:
                    prev_x, prev_y = arr[i-1]
                    if abs(x - prev_x) < 30 and abs(y - prev_y) < 30:
                        merged_x = (x + prev_x) / 2
                        merged_y = (y + prev_y) / 2
                        merged_points[-1] = [merged_x, merged_y]
                        point_counts[(merged_x, merged_y)] += 1
                        merged = True
                if not merged:
                    merged_points.append([x, y])
                    point_counts[(x, y)] += 1
            sorted_points = sorted(point_counts.items(), key=lambda x: x[1], reverse=True)
            ret = [list(point) for point in sorted_points[:2]]
            ret_edit = []
            for i in range(len(ret)):
                tmp0 = ret[i][0][0]
                tmp1 = ret[i][0][1]
                ret_edit.append([tmp0,tmp1])
            return ret_edit
        else:
            ret_edit = []
            return ret_edit

# test = radar_cv()
# img = cv2.imread('radar_map.jpg')
# while True:
#     res = test.filt(img)
#     print(res)
#     time.sleep(0.05)


# cv2.imshow("Result", res)
# cv2.waitKey(0)
# cv2.destroyAllWindows()