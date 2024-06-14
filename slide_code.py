class Slider:
    def is_pixel_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param img1: 图片1
        :param img2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pix1 = img1.load()[x - 1, y - 1]
        pix2 = img2.load()[x - 1, y - 1]
        threshold = 60
        if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(
                pix1[2] - pix2[2] < threshold)):
            return True
        else:
            return False

    def get_gap(self, img1, img2):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图片
        :return:
        """
        left = 0
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    return left
        return 0


import cv2
import numpy as np
from PIL import Image

image_path = 'test.png'
image1_path = 'test1.png'


# 通过轮廓相似度匹配
def contour_match():
    pass


# slider = Slider()
# image = Image.open(image_path).resize((242, 94))
# image1 = Image.open(image1_path).resize((34, 34))
# left = slider.get_gap(image1, image)
# print(left)

image = cv2.resize(cv2.imread(image_path), (242, 94))
image1 = cv2.resize(cv2.imread(image1_path), (34, 34))
# 高斯滤波
blurred1 = cv2.GaussianBlur(image1, (5, 5), 0)
# 图像二值化
target_canny = cv2.Canny(blurred1, 200, 400)
# cv2.imshow("canny", target_canny)
target_contours, target_hierarchy = cv2.findContours(target_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# for i, contour in enumerate(target_contours):
#     print(contour.size)
#     x, y, w, h = cv2.boundingRect(contour)
#     image1 = cv2.resize(cv2.imread(image1_path), (34, 34))
#     cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)
#     cv2.imshow(str(i), image1)
#     cv2.waitKey(0)


# 选择缺口轮廓 最大的轮廓
target_contours_max = max(target_contours, key=lambda x: x.size)

# 高斯滤波
blurred = cv2.GaussianBlur(image, (5, 5), 0)
# 图像二值化
canny = cv2.Canny(blurred, 200, 400)

# 提取边缘轮廓  参数说明 分别为: 二值图像, 只检测最外围轮廓, 仅保存轮廓的拐点信息
contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
target_moments = cv2.moments(target_contours_max)
if target_moments['m00'] == 0:
    target_cx, target_cy = 0, 0
else:
    target_cx, target_cy = target_moments['m10'] / target_moments['m00'], target_moments['m01'] / target_moments['m00']

count = 0
for contour in contours:
    print(count)
    image = cv2.resize(cv2.imread(image_path), (242, 94))
    x, y, w, h = cv2.boundingRect(contours[count])
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow(str(count), image)
    cv2.waitKey(0)
    # 3.创建计算距离对象
    hausdorff_sd = cv2.createHausdorffDistanceExtractor()
    d1 = hausdorff_sd.computeDistance(target_contours_max, contour)
    print(d1)
    count += 1
x, y, w, h = cv2.boundingRect(contours[7])
print(x, y)
# for i, contour in enumerate(contours):  # 所有轮廓
#     x, y, w, h = cv2.boundingRect(contour)  # 外接矩形
#     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
#     cv2.imshow(str(i), image)
#     cv2.waitKey(0)
#     print(i)

# d_value_list = []
# x, y, w, h = 0, 0, 0, 0
# for i, contour in enumerate(contours):
#     M = cv2.moments(contour)
#     if M['m00'] == 0:
#         cx, cy = 0, 0
#     else:
#         # 重心
#         cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
#     d_value_area = abs(cv2.contourArea(contour)-cv2.contourArea(target_contours[1]))
#     d_value_len = abs(cv2.arcLength(contour, True)-cv2.arcLength(target_contours[1], True))
#     d_value_cx = abs(cx - target_cx) + abs(cy - target_cy)
#     print(i, d_value_area, d_value_len, d_value_cx)
# if d_value_area < 50 and d_value_len < 200 and d_value_cx < 250:  # 计算轮廓的面积
#     print(i, d_value_area, d_value_len, d_value_cx)
#     x, y, w, h = cv2.boundingRect(contour)
# image = cv2.resize(cv2.imread(image_path), (242, 94))
# cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
# cv2.imshow(str(i), image)
# cv2.waitKey(0)

# print(x, y)
# cv2.waitKey(0)
