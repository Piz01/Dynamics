#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from rclpy.qos import qos_profile_sensor_data

class FakeJointStatePublisher(Node):
    def __init__(self):
        super().__init__('fake_joint_state_publisher')
        self.publisher_ = self.create_publisher(JointState, '/joint_states', qos_profile_sensor_data)
        self.timer = self.create_timer(0.1, self.timer_callback)  # Pubblica ogni 0.1 secondi
        # Definisci i nomi dei giunti che corrispondono alla configurazione del tuo robot
        self.joint_names = ['elbow_1_joint', 'shoulder_1_joint', 'shoulder_2_joint', 'wrist_1_joint', 'wrist_2_joint']
        # Imposta posizioni iniziali (puoi modificarle in base allo stato "home" o a quello attuale)
        self.joint_positions = [0.0 for _ in self.joint_names]

    def timer_callback(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = self.joint_positions
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing fake joint state')

def main(args=None):
    rclpy.init(args=args)
    node = FakeJointStatePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

