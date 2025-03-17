import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class JointTrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('joint_trajectory_publisher')
        self.publisher_ = self.create_publisher(JointTrajectory, '/manipulator_controller/joint_trajectory', 10)
        self.timer = self.create_timer(1.0, self.send_command)

    def send_command(self):
        msg = JointTrajectory()
        msg.joint_names = ['shoulder_1_joint']  # Nome del giunto da muovere

        point = JointTrajectoryPoint()
        point.positions = [1.0]  # Angolo desiderato in radianti
        point.time_from_start.sec = 2  # Tempo per raggiungere la posizione (2 secondi)

        msg.points.append(point)
        self.publisher_.publish(msg)
        self.get_logger().info('Sent joint trajectory command')

rclpy.init()
node = JointTrajectoryPublisher()
rclpy.spin(node)
node.destroy_node()
rclpy.shutdown()
