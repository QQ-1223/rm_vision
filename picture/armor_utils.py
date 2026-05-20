import cv2
import numpy as np
from config import *

# 预处理函数（HSV+形态学）
def preprocess(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 蓝色装甲板阈值
    lower_blue = np.array([85, 45, 110], dtype=np.uint8) 
    upper_blue = np.array([135, 210, 255], dtype=np.uint8) 

    # 提取蓝色区域
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 形态学操作
    kernel_close = np.ones((4, 4), dtype=np.uint8)
    kernel_open = np.ones((3, 3), dtype=np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)

    return mask

# 轮廓筛选函数
def find_contours(binary, frame): 
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    length = len(contours)
    data_list = []

    if length > 0:
        for contour in contours:
            data_dict = dict()
            
            # 面积过滤
            area = cv2.contourArea(contour)
            if area < MIN_AREA or area > 3000: 
                continue

            # 最小外接矩形
            rect = cv2.minAreaRect(contour)
            rx, ry = rect[0]
            rw = rect[1][0]
            rh = rect[1][1]
            angle = rect[2]
            coor = cv2.boxPoints(rect)
            coor = np.int0(coor)

            # 跳过零尺寸
            if rw == 0 or rh == 0:
                continue
                
            # 最小尺寸过滤
            if rw < 6 or rh < 12:
                continue
                
            # 长宽比过滤
            ratio = max(rw, rh) / min(rw, rh)
            if not (RATIO_MIN < ratio < RATIO_MAX):
                continue
                
            # 角度过滤（灯条应该接近垂直或水平）
            if angle < -45:
                angle += 90
            abs_angle = abs(angle)
            if not (abs_angle < 40 or abs_angle > 50):
                continue

            # 矩形度过滤
            rect_area = rw * rh
            solidity = area / rect_area
            if solidity < 0.4:
                continue

            # 存入字典
            data_dict["rect"] = rect
            data_dict["box"] = coor
            data_dict["ry"] = ry
            data_dict["center"] = (rx, ry)
            data_dict["area"] = area
            data_dict["w"] = rw
            data_dict["h"] = rh
            data_dict["angle"] = angle
            data_list.append(data_dict)
    
    return data_list

# 灯条配对函数 
def pair_armors(valid_bars):
    armors = []
    n = len(valid_bars)
    for i in range(n):
        for j in range(i + 1, n):
            b1 = valid_bars[i]
            b2 = valid_bars[j]
            
            # 计算水平距离
            dx = abs(b1["center"][0] - b2["center"][0])
            if dx < 10 or dx > 300: 
                continue
                
            # 垂直偏移过滤
            dy = abs(b1["center"][1] - b2["center"][1])
            if dy > DY_LIMIT * 1.5:  # 大幅放宽：乘以1.5
                continue

            # 面积差过滤
            area_diff = abs(b1["area"] - b2["area"]) / max(b1["area"], b2["area"])
            if area_diff > AREA_RATIO_LIMIT + 0.2: 
                continue
                
            # 宽度差过滤
            w_diff = abs(b1["w"] - b2["w"]) / max(b1["w"], b2["w"])
            if w_diff > 0.6: 
                continue
                
            # 高度差过滤
            h_diff = abs(b1["h"] - b2["h"]) / max(b1["h"], b2["h"])
            if h_diff > 0.6:  
                continue
                
            # 角度差过滤
            angle_diff = abs(b1["angle"] - b2["angle"])
            if angle_diff > 20: 
                continue

            # 装甲板长宽比约束
            bar_height = max(b1["h"], b2["h"])
            armor_ratio = dx / bar_height
            if armor_ratio < 1.2 or armor_ratio > 5:
                continue

            # 装甲板中心计算
            cx = (b1["center"][0] + b2["center"][0]) / 2
            cy = (b1["center"][1] + b2["center"][1]) / 2
            armors.append({
                "bar1": b1,
                "bar2": b2,
                "center": (cx, cy)
            })
    return armors