import rclpy  #导入python库,所有节点都要用
from rclpy.node import Node #Node是节点的基础模板
 
from my_interfaces.msg import MyMessage
 
 
class SubscriberNode(Node):
 
    def __init__(self):
        super().__init__('subscriber') #命名节点为”subscriber“
        self.subscription = self.create_subscription(
            MyMessage,  # 消息类型
            'topic',  # 话题名称
            self.listener_callback, #回调函数
            10 # Qos profile（队列深度）
        )
 
    def listener_callback(self,msg):
        self.get_logger().info(
            f'I heard:name = "{msg.name}",age = {msg.age}'
        )

    #def callback(self, msg):
        #print(f'I heard:name = "{msg.name}",age = {msg.age}')


def main(args=None):
        rclpy.init(args=args)
        node = SubscriberNode()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()
 
 
if __name__ == '__main__':
    main()