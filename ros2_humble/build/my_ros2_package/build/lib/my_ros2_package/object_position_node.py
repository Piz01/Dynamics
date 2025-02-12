import rclpy
from rclpy.node import Node
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose

class PoseListener(Node):
    def __init__(self):
        super().__init__('pose_listener')
        self.subscription = self.create_subscription(
            Pose,
            'Cube',  # Deve corrispondere al topic usato in Unity
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self, msg):
        self.get_logger().info(f'Posizione ricevuta: x={msg.position.x}, y={msg.position.y}, z={msg.position.z}')
        self.get_logger().info(f'Orientamento ricevuto: x={msg.orientation.x}, y={msg.orientation.y}, z={msg.orientation.z}, w={msg.orientation.w}')

def main(args=None):
    rclpy.init(args=args)
    node = PoseListener()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

