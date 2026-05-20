# test - 颜色阈值调试工具

## 功能说明

本文件夹包含基于 OpenCV 的颜色阈值调试工具，用于实时调整 HSV 参数和形态学处理参数，帮助用户找到最佳的颜色识别配置。

## 功能列表

| 文件 | 功能 |
|------|------|
| `picture test.py` | 图片颜色阈值调试工具 |
| `video test.py` | 视频颜色阈值调试工具 |

### 核心功能
- **HSV 颜色空间分割**：通过滑动条实时调整 Hue、Saturation、Value 阈值
- **形态学处理**：支持开运算、闭运算、腐蚀、膨胀四种操作
- **实时预览**：即时查看颜色分割和形态学处理效果

## 操作方法

### 运行图片测试
```bash
cd /home/liu/RM_Vision/zhuangjiaban/test
python "picture test.py"
```

### 运行视频测试
```bash
cd /home/liu/RM_Vision/zhuangjiaban/test
python "video test.py"
```

### 调整参数
1. **color_adjust 窗口**：调整 HSV 颜色阈值
   - hmin/hmax: Hue 范围 (0-179)
   - smin/smax: Saturation 范围 (0-255)
   - vmin/vmax: Value 范围 (0-255)

2. **mor_adjust 窗口**：调整形态学参数
   - open/open_k: 开运算核大小
   - close/close_k: 闭运算核大小
   - erode/erode_k: 腐蚀核大小
   - dilate/dilate_k: 膨胀核大小

3. **结果窗口**：
   - 原始画面：显示缩放后的原始图像/视频帧
   - 掩码：显示 HSV 颜色分割结果
   - 形态学处理：显示经过形态学操作后的最终结果

### 退出
按 `q` 键退出程序。

## 依赖
```bash
pip install opencv-python numpy
```
