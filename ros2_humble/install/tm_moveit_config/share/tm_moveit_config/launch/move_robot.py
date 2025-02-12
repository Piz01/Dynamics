#!/usr/bin/env python3
"""
Nodo ROS2 che utilizza MoveIt per spostare il robot dalla posizione "home" a "work".
Assicurati che i named target "home" e "work" siano definiti nel tuo MoveIt configuration package.
"""

import sys
import rclpy
from rclpy.node import Node

# Importa le classi di moveit_commander
from moveit_commander import MoveGroupCommander, RobotCommander, PlanningSceneInterface, roscpp_initialize, roscpp_shutdown

class MoveRobot(Node):
    def __init__(self):
        super().__init__('move_robot_node')
        self.get_logger().info("Inizializzazione MoveIt")
        # Inizializza i componenti di MoveIt
        self.robot = RobotCommander()
        self.scene = PlanningSceneInterface()
        self.group = MoveGroupCommander("manipulator")  # Assicurati che il nome corrisponda al gruppo definito

    def move_to_named_target(self, target_name):
        self.get_logger().info(f"Muovo il robot verso la posizione '{target_name}'...")
        self.group.set_named_target(target_name)
        plan = self.group.plan()
        if plan and len(plan.joint_trajectory.points) > 0:
            self.group.execute(plan, wait=True)
            self.get_logger().info(f"Posizione '{target_name}' raggiunta.")
        else:
            self.get_logger().error(f"Impossibile pianificare il movimento verso '{target_name}'.")

def main(args=None):
    roscpp_initialize(sys.argv)
    rclpy.init(args=args)
    
    move_robot_node = MoveRobot()
    
    # Muovi il robot prima alla posizione "home"
    move_robot_node.move_to_named_target("home")
    
    # Attendi qualche secondo (opzionale) prima del movimento successivo
    move_robot_node.get_logger().info("Attendo 2 secondi prima di passare alla posizione 'work'...")
    move_robot_node.create_timer(2.0, lambda: None)  # Timer fittizio per dare una pausa

    # Muovi il robot alla posizione "work"
    move_robot_node.move_to_named_target("work")
    
    # Chiudi il nodo
    move_robot_node.get_logger().info("Movimento completato.")
    move_robot_node.destroy_node()
    rclpy.shutdown()
    roscpp_shutdown()

if __name__ == '__main__':
    main()

