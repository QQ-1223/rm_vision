# rm_vision phase0

## 环境
Ubuntu 22.04
ROS2 Humble
Python 3.10

## 搭建步骤
cd ~/ros2_ws1
colcon build --packages-select my_interfaces
colcon build --packages-select py_pubsub
source install/setup.bash

## 运行方法
### 方法一（分别运行两个终端）
#### 终端1
ros2 run py_pubsub talker
#### 终端2
ros2 run py_pubsub listener

### 方法二（运行launch）
ros2 launch py_pubsub my_launch.py
