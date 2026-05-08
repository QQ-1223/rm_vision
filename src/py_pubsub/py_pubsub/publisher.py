import rclpy  #导入python库,所有节点都要用
from rclpy.node import Node #Node是节点的基础模板
 
from my_interfaces.msg import MyMessage

import random #导入随机数
 
 
class PublisherNode(Node):
 
    def __init__(self):
        super().__init__('publisher') #命名节点为”publisher“
        self.publisher = self.create_publisher(MyMessage, 'topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback) #每隔一秒执行一次函数
 
    def timer_callback(self):
        msg = MyMessage()
        msg.name = "robot_01"
        msg.age = random.randint(15,35) #随即生成15-35之间的数
        if msg.age > 25:
            self.get_logger().info(f'射速过快！当前射速:{msg.age}m/s')
        else:
            self.get_logger().info(f'射速正常。当前射速:{msg.age}m/s')

        self.publisher.publish(msg) #发送
 
    

def main():
    rclpy.init()
    publisher = PublisherNode()
    rclpy.spin(publisher)
    publisher.destroy_node()
    rclpy.shutdown()
 
 
if __name__ == '__main__':
    main()