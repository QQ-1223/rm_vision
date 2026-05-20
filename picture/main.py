import cv2
import numpy as np
from armor_utils import preprocess, find_contours, pair_armors

# 主函数（图片识别模式）
def main():
    # 图片文件路径
    photo = '/home/liu/RM_Vision/zhuangjiaban/picture/blue.jpeg' 
    frame = cv2.imread(photo)

    if frame is None:
        print("无法打开图片文件")
        return

    # 预处理
    mask = preprocess(frame)
    draw = frame.copy()

    try:
        # 查找灯条
        valid_bars = find_contours(mask, frame)

        # 灯条配对
        if not valid_bars:
            armors = []
        else:
            armors = pair_armors(valid_bars)

        # 绘制灯条（绿色）
        for bar in valid_bars:
            cv2.drawContours(draw, [bar["box"]], 0, (0, 255, 0), 2)

        # 绘制装甲板（红色）
        for armor in armors:
            bar1 = armor["bar1"]
            bar2 = armor["bar2"]
            pts = np.concatenate([bar1["box"], bar2["box"]])
            rect = cv2.minAreaRect(pts)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(draw, [box], 0, (0, 0, 255), 2)

            cx, cy = map(int, armor["center"])
            cv2.circle(draw, (cx, cy), 5, (255, 0, 0), -1)
            cv2.putText(draw, "Armor", (cx-20, cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            print(f"装甲板中心位置: ({cx}, {cy})")

    except Exception as e:
        print(f"处理错误: {e}")

    # 显示结果
    cv2.imshow("掩码", mask)
    cv2.imshow("识别结果", draw)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("已释放所有资源")

if __name__ == "__main__":
    main()