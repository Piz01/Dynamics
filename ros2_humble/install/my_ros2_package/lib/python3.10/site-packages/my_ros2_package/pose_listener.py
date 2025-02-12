import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose

class PoseListener(Node):
    def __init__(self):
        super().__init__('pose_listener')
        self.subscription = self.create_subscription(
            Pose,
            'object_pose',
            self.pose_callback,
            10
        )
        self.subscription  
        self.get_logger().info('Il nodo sta ascoltando "object_pose".')

    def pose_callback(self, msg):
        x = f"{msg.position.x:.2f}"
        y = f"{msg.position.y:.2f}"
        z = f"{msg.position.z:.2f}"

        self.get_logger().info(f'Coordinate ricevute: x={x}, y={y}, z={z}')

def main(args=None):
    rclpy.init(args=args)
    node = PoseListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Il nodo ha smesso di ascoltare "object_pose".')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

