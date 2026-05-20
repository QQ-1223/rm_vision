# video - 装甲板视频识别模块

## 功能说明

本模块用于实时识别视频流中的装甲板目标，支持视频文件播放和循环播放，通过计算机视觉技术实现装甲板的实时检测与定位。

## 功能列表

| 文件 | 功能 |
|------|------|
| `main.py` | 主程序入口，处理视频流并显示识别结果 |
| `armor_utils.py` | 工具函数（预处理、轮廓检测、灯条配对） |
| `config.py` | 配置参数文件（HSV阈值、形态学参数、筛选阈值） |

### 核心功能
- **视频流处理**：支持读取本地视频文件，自适应帧率播放
- **HSV 颜色空间分割**：基于配置文件的颜色阈值设定
- **形态学处理**：开运算、闭运算、腐蚀、膨胀操作
- **轮廓筛选**：基于面积、长宽比、角度等特征筛选灯条
- **灯条配对**：将灯条配对形成装甲板
- **实时输出**：控制台输出装甲板中心坐标

## 操作方法

### 运行程序
```bash
cd /home/liu/RM_Vision/zhuangjiaban/video
python main.py
```

### 调整参数
编辑 `config.py` 文件修改以下参数：
- **HSV 阈值**：H_MIN, H_MAX, S_MIN, S_MAX, V_MIN, V_MAX
- **形态学参数**：OPEN_K, CLOSE_K, ERODE_K, DILATE_K
- **筛选阈值**：MIN_AREA, RATIO_MIN, RATIO_MAX, DY_LIMIT, AREA_RATIO_LIMIT

### 切换视频文件
修改 `main.py` 中的视频路径：
```python
video = '/home/liu/RM_Vision/zhuangjiaban/video/video.mp4'
video = '/home/liu/RM_Vision/zhuangjiaban/video/video1.mp4'
video = '/home/liu/RM_Vision/zhuangjiaban/video/video2.mp4'
video = '/home/liu/RM_Vision/zhuangjiaban/video/video3.mp4'
```

### 切换颜色配置
编辑 `config.py` 文件：
```python
# 红色配置
H_MIN, H_MAX = 0, 180
S_MIN, S_MAX = 3, 255
V_MIN, V_MAX = 212, 255

# 蓝色配置
# H_MIN, H_MAX = 90, 130
# S_MIN, S_MAX = 80, 255
# V_MIN, V_MAX = 80, 255
```

### 结果窗口
- **识别结果**：显示装甲板识别结果（绿色框为灯条，红色框为装甲板）
- **掩码**：显示二值化处理后的掩码

### 退出
按 `q` 键退出程序。

## 依赖
```bash
pip install opencv-python numpy
```
