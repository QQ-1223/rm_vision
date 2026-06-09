# 阶段2考核项目说明文档

## 一、项目概述

本项目基于 YOLOv8目标检测框架，实现了对"红甲"（Red Armor）和"蓝甲"（Blue Armor）两类目标的检测任务。通过训练自定义数据集，构建了一个能够在视频中实时识别这两类装甲目标的模型。


## 二、做了什么

### 1. 任务目标
- 构建基于YOLOv8的目标检测模型
- 识别两类目标：红甲（Red Armor）、蓝甲（Blue Armor）
- 实现视频流实时推理检测

### 2. 完成的工作
数据集配置:配置了包含2类目标的数据集（bvn.yaml） 
模型训练:使用YOLOv8训练了30个epoch，得到最佳权重（best.pt）
视频推理:实现了视频文件的目标检测推理脚本 
结果输出:生成了推理结果视频（result.mp4）和测试结果图片 


## 三、怎么做

### 1. 环境配置
- 框架：Ultralytics YOLOv8
- 语言：Python

### 2. 数据集准备

数据集配置文件 `bvn.yaml` 定义了：
- 数据集根路径：`/mnt/ubuntu_data/yolov8/datasets/bvn`
- 训练集路径：`train/images`
- 验证集路径：`val/images`
- 类别数量：2类
- 类别名称：`['Red Armor', 'Blue Armor']`

### 3. 模型训练

训练参数配置（args.yaml）：
| 参数 | 值 | 说明 |
|-----|-----|------|
| epochs | 30 | 训练轮数 |
| batch | 8 | 批次大小 |
| imgsz | 640 | 输入图像尺寸 |
| device | cpu | 训练设备 |
| lr0 | 0.01 | 初始学习率 |
| resume | last.pt | 断点续训 |

训练启动：
```bash
python train.py --data bvn.yaml --epochs 30
```

### 4. 视频推理

推理脚本 `video_infer.py` 实现流程：
1. 加载训练好的模型权重（best.pt）
2. 读取测试视频文件（test.mp4）
3. 执行目标检测推理（置信度阈值0.25）
4. 保存检测结果视频

```python
from ultralytics import YOLO

# 加载训练好的模型
model = YOLO("./weights/best.pt")
# 测试视频
video_path = "./test.mp4"
# 推理
model.predict(source=video_path, save=True, save_conf=True, conf=0.25)
```


## 四、遇到的问题及解决方案

问题1：推理置信度阈值设置
问题描述:置信度阈值（conf=0.25）较低可能导致误检
解决方案:可根据实际检测效果调整阈值（建议范围：0.3~0.5）

问题2：大文件上传限制
问题描述：仓库内包含演示视频和result视频，超过github上传限制
解决方案：尝试用Git LFS上传但失败，最终选择将文件上传到网盘


## 五、使用说明

### 训练
```bash
cd submit/train_config
bash train.sh
```

### 推理
```bash
cd submit/inference
python video_infer.py
```

### 注意事项
1. 确保 `ultralytics` 库已正确安装
2. 数据集路径需与实际存放位置一致
3. 推理时需确保 `weights/best.pt` 存在
