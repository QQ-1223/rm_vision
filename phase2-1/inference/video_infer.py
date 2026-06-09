from ultralytics import YOLO

#加载训练好的模型
model = YOLO("./weights/best.pt")
#测试视频
video_path = "./test.mp4"
#推理
model.predict(source=video_path,save=True,save_conf=True,conf=0.25)

