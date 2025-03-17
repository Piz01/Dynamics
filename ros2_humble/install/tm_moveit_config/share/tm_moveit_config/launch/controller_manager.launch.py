import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Recupera il percorso del package e del file URDF
    pkg_share_urdf = get_package_share_directory('tm_description')
    pkg_share_controller = get_package_share_directory('tm_moveit_config')
    urdf_file = os.path.join(pkg_share_urdf, 'urdf', 'tm900_robot_prova2.urdf')
    
    # Legge il contenuto del file URDF
    with open(urdf_file, 'r') as file:
        robot_description = file.read()
    
    # Percorso del file di configurazione ros2_controllers.yaml
    controller_config = os.path.join(pkg_share_controller, 'config', 'ros2_controllers.yaml')

    return LaunchDescription([
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[{'robot_description': robot_description, 'use_sim_time': True}, controller_config],
            output='screen'
        ),
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['manipulator_controller'],
            output='screen'
        ),
    ])
