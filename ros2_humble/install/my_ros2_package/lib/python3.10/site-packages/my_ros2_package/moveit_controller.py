#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, JointConstraint
from trajectory_msgs.msg import JointTrajectory

class MoveItTrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('moveit_trajectory_publisher')
        # Publisher per inviare la traiettoria a Unity
        self.trajectory_pub = self.create_publisher(JointTrajectory, '/manipulator_controller/joint_trajectory', 10)
        # Action client per il MoveGroup (assumiamo che l'action server si chiami 'move_action')
        self._action_client = ActionClient(self, MoveGroup, 'move_action')
        self.send_goal()

    def send_goal(self):
        goal_msg = MoveGroup.Goal()
        # Imposta il nome del gruppo come definito nella configurazione MoveIt
        goal_msg.request.group_name = "manipulator"
        # Utilizza lo stato attuale come start state (assumendo che il robot sia in "home")
        goal_msg.request.start_state.is_diff = True
        
        # Costruisci i constraints per la posa "work" (valori presi dal tuo SRDF)
        constraints = Constraints()
        joint_targets = {
            "elbow_1_joint": 0.9633,
            "shoulder_1_joint": 0.0,
            "shoulder_2_joint": 0.755,
            "wrist_1_joint": 1.2844,
            "wrist_2_joint": -0.1736
        }
        for joint_name, target_value in joint_targets.items():
            jc = JointConstraint()
            jc.joint_name = joint_name
            jc.position = target_value
            jc.tolerance_above = 0.1
            jc.tolerance_below = 0.1
            jc.weight = 1.0
            constraints.joint_constraints.append(jc)
        
        goal_msg.request.goal_constraints = [constraints]
        # Pianifica (plan_only) per ottenere la traiettoria senza farla eseguire direttamente da MoveIt
        goal_msg.planning_options.plan_only = True
        
        self.get_logger().info("Invio goal a MoveIt per pianificare la traiettoria verso 'work'...")
        self._action_client.wait_for_server()
        self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)\
            .add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info("Feedback ricevuto.")

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("Goal rifiutato dal server MoveIt.")
            return
        self.get_logger().info("Goal accettato, attendo il risultato...")
        goal_handle.get_result_async().add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        trajectory = result.planned_trajectory.joint_trajectory
        if trajectory:
            self.trajectory_pub.publish(trajectory)
            self.get_logger().info("Traiettoria pianificata pubblicata sul topic per Unity.")
        else:
            self.get_logger().error("Nessuna traiettoria trovata.")
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = MoveItTrajectoryPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
