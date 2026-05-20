import cv2
import numpy as np

WIDTH = 640
HIGH = 480

def nothing(x):
    pass

def creatTrackbar():  # creat trackbar to adjust the color threshold.
    # blue
    # cv.createTrackbar("hmin", "color_adjust", 0, 255, nothing)
    # cv.createTrackbar("hmax", "color_adjust", 250, 255, nothing)
    # cv.createTrackbar("smin", "color_adjust", 0, 255, nothing)
    # cv.createTrackbar("smax", "color_adjust", 143, 255, nothing)
    # cv.createTrackbar("vmin", "color_adjust", 255, 255, nothing)
    # cv.createTrackbar("vmax", "color_adjust", 255, 255, nothing)
    # red
    cv2.createTrackbar("hmin", "color_adjust", 0, 255, nothing)
    cv2.createTrackbar("hmax", "color_adjust", 255, 255, nothing)
    cv2.createTrackbar("smin", "color_adjust", 3, 255, nothing)
    cv2.createTrackbar("smax", "color_adjust", 255, 255, nothing)
    cv2.createTrackbar("vmin", "color_adjust", 245, 255, nothing)
    cv2.createTrackbar("vmax", "color_adjust", 255, 255, nothing)

    cv2.createTrackbar("open", "mor_adjust", 1, 30, nothing)
    cv2.createTrackbar("close", "mor_adjust", 5, 30, nothing)
    cv2.createTrackbar("erode", "mor_adjust", 2, 30, nothing)
    cv2.createTrackbar("dilate", "mor_adjust", 5, 30, nothing)


def hsv_change(frame):  # hsv channel separation.
    hmin = cv2.getTrackbarPos('hmin', 'color_adjust')
    hmax = cv2.getTrackbarPos('hmax', 'color_adjust')
    smin = cv2.getTrackbarPos('smin', 'color_adjust')
    smax = cv2.getTrackbarPos('smax', 'color_adjust')
    vmin = cv2.getTrackbarPos('vmin', 'color_adjust')
    vmax = cv2.getTrackbarPos('vmax', 'color_adjust')

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray", gray)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([hmin, smin, vmin])
    upper_hsv = np.array([hmax, smax, vmax])
    mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    return mask

def open_binary(binary, x, y):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (x, y))
    dst = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    return dst


def close_binary(binary, x, y):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (x, y))
    dst = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return dst


def erode_binary(binary, x, y):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (x, y))
    dst = cv2.erode(binary, kernel)
    return dst


def dilate_binary(binary, x, y):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (x, y))
    dst = cv2.dilate(binary, kernel)
    return dst

if __name__ == '__main__':
    photo = 'red.jpeg' #视频文件路径
    cap = cv2.imread(photo) #创建视频捕获对象，打开视频文件
    if cap is None:
        print("无法打开视频文件")
        exit()
    #创建窗口和滑动条
    cv2.namedWindow("color_adjust")
    cv2.namedWindow("mor_adjust")
    creatTrackbar() #创建调节颜色阈值和形态学参数的滑动条

    while True:
        open = cv2.getTrackbarPos('open', 'mor_adjust')
        close = cv2.getTrackbarPos('close', 'mor_adjust')
        erode = cv2.getTrackbarPos('erode', 'mor_adjust')
        dilate = cv2.getTrackbarPos('dilate', 'mor_adjust')
        frame = cv2.resize(cap, (WIDTH, HIGH), interpolation=cv2.INTER_CUBIC) 
        #把frame缩放到WIDTH*HIGH大小，插值方法为INTER_CUBIC（三次插值算法）

        mask = hsv_change(frame) #BGR转HSV，进行颜色空间分割（只保留目标颜色的二值图像），得到二值化的掩码
        dst_open = open_binary(mask, open, open) #调用open_binary函数做开运算（先腐蚀后膨胀），去除小的噪点
        dst_close = close_binary(mask, close, close) #调用close_binary函数做闭运算（先膨胀后腐蚀），填充小的孔洞
        dst_erode = erode_binary(dst_close, erode, erode) #腐蚀
        dst_dilate = dilate_binary(dst_erode, dilate, dilate) #膨胀
        cv2.circle(frame, (int(WIDTH / 2), int(HIGH / 2)), 2, (255, 0, 255), -1)

        cv2.imshow("原始画面", frame) #显示经过形态学处理后的二值图像
        cv2.imshow("掩码", mask) #显示原始帧（缩放后）
        cv2.imshow("形态学处理", dst_dilate) #显示原始帧（缩放后）

        if cv2.waitKey(1) & 0xFF == ord('q'): #按'q'键退出循环
            break

    cv2.destroyAllWindows() #关闭所有窗口