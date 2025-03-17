import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Percorso al tuo file URDF
    urdf_file = os.path.join(get_package_share_directory('tm_description'), 'urdf', 'tm900_robot_prova2.urdf')
    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()
    
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
        ),
    ])

