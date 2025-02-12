#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState

class MoveRobot(Node):
    def __init__(self):
        super().__init__("move_robot")
        
        # Inizializza MoveItPy
        self.moveit = MoveItPy(node_name="move_robot")

        # Definisce il gruppo di manipolazione (cambia con il nome esatto del tuo gruppo)
        self.arm = self.moveit.get_planning_component("manipulator")

        # Definisce le pose di "home" e "work"
        self.home_pose = [0.0, -1.57, 1.57, 0.0, 1.57, 0.0]  # Modifica con i tuoi valori reali
        self.work_pose = [0.5, -1.0, 1.2, 0.0, 1.3, 0.2]  # Modifica con i tuoi valori reali

    def move_to_home(self):
        self.get_logger().info("Spostamento in posizione home...")
        self.arm.set_joint_target(self.home_pose)
        self.arm.plan()
        self.arm.execute()

    def move_to_work(self):
        self.get_logger().info("Spostamento in posizione work...")
        self.arm.set_joint_target(self.work_pose)
        self.arm.plan()
        self.arm.execute()

def main():
    rclpy.init()
    node = MoveRobot()

    node.move_to_home()
    node.move_to_work()

    rclpy.shutdown()

if __name__ == "__main__":
    main()

