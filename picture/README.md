# picture - 装甲板图片识别模块

## 功能说明

本模块用于识别图片中的装甲板目标，通过轮廓检测和灯条配对算法实现装甲板定位。

## 功能列表

| 文件 | 功能 |
|------|------|
| `main.py` | 主程序入口，处理图片并显示识别结果 |
| `armor_utils.py` | 工具函数（预处理、轮廓检测、灯条配对） |
| `config.py` | 配置参数文件（HSV阈值、形态学参数、筛选阈值） |

### 核心功能
- **HSV 颜色空间分割**：调整颜色阈值
- **形态学处理**：开运算去噪、闭运算填洞、腐蚀膨胀优化
- **轮廓筛选**：基于面积、长宽比、角度等特征筛选灯条
- **灯条配对**：将符合条件的灯条配对形成装甲板
- **结果标注**：绘制灯条和装甲板位置，显示中心坐标

## 操作方法

### 运行程序
```bash
cd /home/liu/RM_Vision/zhuangjiaban/picture
python main.py
```

### 调整参数
 **结果窗口**：
   - 掩码：显示二值化处理结果
   - 识别结果：显示灯条（绿色框）和装甲板（红色框）

### 切换颜色配置
编辑 `config.py` 文件，注释掉当前颜色配置，取消注释目标颜色配置：
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

同时修改 `main.py` 中的图片路径：
```python
photo = '/home/liu/RM_Vision/zhuangjiaban/picture/red.jpeg'
```

### 退出
按 `q` 键退出程序。

## 依赖
```bash
pip install opencv-python numpy
```
