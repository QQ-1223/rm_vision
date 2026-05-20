import cv2
import numpy as np # 导入Numpy库，用于创建数组（HSV上下限）

# 定义图像缩放的宽和高
WIDTH = 640
HIGH = 480

#空回调函数，trackbar必须绑定一个回调函数，但我们不需要在回调函数中执行任何操作，所以定义一个空函数pass占位
def nothing(x):
    pass

# 创建滑动条的函数，用于调整颜色阈值和形态学操作的参数
def creatTrackbar():  #cv2.createTracker(名称，窗口名，默认值，最大值，回调函数)
    # HSV三通道上下限 Hue（色调）范围0-179，Saturation（饱和度）范围0-255，Value（亮度）范围0-255

    # blue的HSV阈值
    # cv.createTrackbar("hmin", "color_adjust", 0, 255, nothing)
    # cv.createTrackbar("hmax", "color_adjust", 250, 255, nothing)
    # cv.createTrackbar("smin", "color_adjust", 0, 255, nothing)
    # cv.createTrackbar("smax", "color_adjust", 143, 255, nothing)
    # cv.createTrackbar("vmin", "color_adjust", 255, 255, nothing)
    # cv.createTrackbar("vmax", "color_adjust", 255, 255, nothing)

    # red的HSV阈值
    cv2.createTrackbar("hmin", "color_adjust", 0, 255, nothing)
    cv2.createTrackbar("hmax", "color_adjust", 255, 255, nothing)
    cv2.createTrackbar("smin", "color_adjust", 3, 255, nothing)
    cv2.createTrackbar("smax", "color_adjust", 255, 255, nothing)
    cv2.createTrackbar("vmin", "color_adjust", 245, 255, nothing)
    cv2.createTrackbar("vmax", "color_adjust", 255, 255, nothing)

    # 形态学参数滑动条（开运算，闭运算，腐蚀，膨胀的核大小）
    cv2.createTrackbar("open_k", "mor_adjust", 1, 30, nothing)
    cv2.createTrackbar("close_k", "mor_adjust", 5, 30, nothing)
    cv2.createTrackbar("erode_k", "mor_adjust", 2, 30, nothing)
    cv2.createTrackbar("dilate_k", "mor_adjust", 5, 30, nothing)


# HSV颜色空间分割函数，根据滑动条设置的HSV阈值创建掩码
def hsv_change(frame): # getTrackbarPos函数获取滑动条的当前值，分别获取hmin、hmax、smin、smax、vmin、vmax
    #cv2.getTrackerPos(滑动条名称，窗口名称) 
    hmin = cv2.getTrackbarPos('hmin', 'color_adjust')
    hmax = cv2.getTrackbarPos('hmax', 'color_adjust')
    smin = cv2.getTrackbarPos('smin', 'color_adjust')
    smax = cv2.getTrackbarPos('smax', 'color_adjust')
    vmin = cv2.getTrackbarPos('vmin', 'color_adjust')
    vmax = cv2.getTrackbarPos('vmax', 'color_adjust')

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray", gray)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # BGR转HSV，HSV更适合做颜色分割
    # 创建HSV阈值的上下限数组，lowerb和upperb参数分别是掩码的下限和上限
    lower_hsv = np.array([hmin, smin, vmin])
    upper_hsv = np.array([hmax, smax, vmax])
    # cv2.inRange函数根据设定的HSV上下限创建二值掩码，掩码中满足条件的像素值为255（白），不满足条件的像素值为0（黑）
    mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    return mask

# 开运算函数，先腐蚀后膨胀，去除小的噪点
def open_binary(binary, x, y):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(x), int(y))) 
    # cv2.getStructuringElement创建一个矩形结构元素，大小由x和y参数决定
    dst = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel) 
    # cv2.morphologyEx函数执行形态学操作，cv2.morphologyEx(输入图像，操作类型（开运算），结构元素)
    # cv2.MORPH_OPEN开运算
    return dst

# 闭运算函数，先膨胀后腐蚀，填充小的孔洞
def close_binary(binary, x, y):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(x), int(y)))
    dst = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel) # cv2.MORPH_CLOSE闭运算
    return dst

# 腐蚀函数，缩小白色区域，去除边界上的像素
def erode_binary(binary, x, y):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(x), int(y)))
    dst = cv2.erode(binary, kernel)
    return dst

# 膨胀函数，扩大白色区域，补洞
def dilate_binary(binary, x, y):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(x), int(y)))
    dst = cv2.dilate(binary, kernel)
    return dst

# 主函数，读取图像，创建窗口和滑动条，循环处理图像并显示结果
if __name__ == '__main__':

    #photo = 'red.jpeg' # 读取图片文件路径
    #cap = cv2.imread(photo) # 创建图像对象，读取图片文件

    video = 'video.mp4' #视频
    cap = cv2.VideoCapture(video)

    #if cap is None: #如果找不到照片，打印错误信息并退出程序
        #print("无法打开文件")
        #exit()

    if not cap.isOpened():
        print("无法打开视频文件")
        exit()
        
    fps = cap.get(cv2.CAP_PROP_FPS) # 获取视频的帧率
    wait_time = int(1000 / fps) # 计算每帧的等待时间，单位为毫秒
  
    #创建两个窗口，一个用于调整颜色阈值，另一个用于调整形态学参数
    cv2.namedWindow("color_adjust")
    cv2.namedWindow("mor_adjust")
    creatTrackbar() #创建滑动条

    # 死循环，持续读取画面、处理、显示，直到用户按下'q'键退出
    while True:

        ret, frame = cap.read() # 读取视频帧，ret是布尔值表示是否成功读取，frame是当前帧的图像数据
        if not ret: # 如果没有成功读取帧，说明视频结束，退出循环
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # 将视频帧位置重置为0，重新播放
            continue
        # 获取形态学参数滑动条的当前值
        open_k = cv2.getTrackbarPos('open_k', 'mor_adjust')
        close_k = cv2.getTrackbarPos('close_k', 'mor_adjust')
        erode_k = cv2.getTrackbarPos('erode_k', 'mor_adjust')
        dilate_k = cv2.getTrackbarPos('dilate_k', 'mor_adjust')

        frame = cv2.resize(frame, (WIDTH, HIGH), interpolation=cv2.INTER_CUBIC) 
        #把cap缩放到WIDTH*HIGH大小，插值方法为INTER_CUBIC（三次插值算法）

        # 颜色分割
        mask = hsv_change(frame) # BGR转HSV，进行颜色空间分割（只保留目标颜色的二值图像），得到二值化的掩码

        # 形态学处理：去噪、填洞
        dst_open = open_binary(mask, open_k, open_k) #调用open_binary函数做开运算（先腐蚀后膨胀），去除小的噪点
        dst_close = close_binary(mask, close_k, close_k) #调用close_binary函数做闭运算（先膨胀后腐蚀），填充小的孔洞
        dst_erode = erode_binary(dst_close, erode_k, erode_k) #腐蚀
        dst_dilate = dilate_binary(dst_erode, dilate_k, dilate_k) #膨胀

        # 在原始帧的中心画一个小圆点，颜色为紫色（BGR格式），半径为2，填充圆点，后续用于做中心追踪的标记
        cv2.circle(frame, (int(WIDTH / 2), int(HIGH / 2)), 2, (255, 0, 255), -1)

        # 显示所有窗口：原始画面（缩放后），掩码（颜色分割结果），形态学处理结果
        cv2.imshow("原始画面", frame) #显示经过形态学处理后的二值图像
        cv2.imshow("掩码", mask) #显示原始帧（缩放后）
        cv2.imshow("形态学处理", dst_dilate) #显示原始帧（缩放后）

        if cv2.waitKey(wait_time) & 0xFF == ord('q'): #按'q'键退出循环
            break

    cv2.destroyAllWindows()