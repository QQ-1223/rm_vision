# HSV颜色过滤参数（与当前Trackbar保持一致）
#red
# H_MIN1, H_MAX1 = 0, 15  
# H_MIN2, H_MAX2 = 165, 180  
# H_MIN,H_MAX = 0, 180  
# S_MIN,S_MAX = 3,255
# V_MIN,V_MAX = 212,255

#blue
H_MIN, H_MAX = 90, 130
S_MIN, S_MAX = 80, 255
V_MIN, V_MAX = 80, 255

# 形态学核的大小
OPEN_K = 1
CLOSE_K = 1
ERODE_K = 0
DILATE_K = 1

# 轮廓筛选/灯条配对阈值
MIN_AREA = 120 
RATIO_MIN = 2.0  
RATIO_MAX = 8
DY_LIMIT = 25  
AREA_RATIO_LIMIT = 0.5  