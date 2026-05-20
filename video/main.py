import cv2
import numpy as np
from armor_utils import preprocess,find_contours,pair_armors

# 主函数
def main():

    video = '/home/liu/RM_Vision/zhuangjiaban/video/video3.mp4' #视频（绝对路径）
    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        print("无法打开视频文件")
        return
        
    # 调整视频播放速度
    fps = cap.get(cv2.CAP_PROP_FPS) # 获取帧率
    if fps <= 0:
        fps = 30 # 防止读取失败
    wait_time = int(1000 / fps) # 计算等待时间
  
    # 死循环
    while True:

        ret, frame = cap.read() # 读取视频帧，ret是布尔值表示是否成功读取，frame是当前帧的图像数据
        if not ret: # 如果没有成功读取帧，说明视频结束，退出循环
            print("视频读取完毕，重新播放")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # 将视频帧位置重置为0，重新播放
            continue
        
        mask = preprocess(frame)
        draw = frame.copy()

        try:
            valid_bars = find_contours(mask,frame)

            if not valid_bars:
                # 没有检测到灯条，仍然显示画面
                armors = []
            else:
                armors = pair_armors(valid_bars) # 灯条配对
        
            for bar in valid_bars:
                cv2.drawContours(draw,[bar["box"]],0,(0,255,0),2)
            
            for armor in armors:
                
                bar1 = armor["bar1"]
                bar2 = armor["bar2"]
                # 构造装甲板四个角点（需要根据实际灯条方向判断顺序）
                pts = np.concatenate([bar1["box"], bar2["box"]])
                rect = cv2.minAreaRect(pts)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(draw, [box], 0, (0, 0, 255), 2)

                cx,cy = map(int,armor["center"])
                cv2.circle(draw,(cx,cy),5,(255,0,0),-1)
                cv2.putText(draw,"Armor",(cx-20,cy-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
                print(f"装甲板中心位置:({cx},{cy})")


        except Exception as e:
            print(f"这一帧处理错误:{e}")

        # 显示所有窗口
        cv2.imshow("识别结果", draw)  # 显示识别结果
        cv2.imshow("掩码", mask)  # 显示颜色分割结果（调试用）
        cv2.imshow("掩码", mask)  # 显示颜色分割结果（调试用）

        if cv2.waitKey(wait_time) & 0xFF == ord('q'): #按'q'键退出循环
            break


    cap.release()
    cv2.destroyAllWindows()
    print("已释放所有资源")

if __name__=="__main__":
    main()