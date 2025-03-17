from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Percorsi dei package
    gazebo_ros_path = get_package_share_directory('gazebo_ros')
    tm_description_path = get_package_share_directory('tm_description')

    return LaunchDescription([
        # Avvia Gazebo con un world vuoto
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(gazebo_ros_path, 'launch', 'empty_world.launch.py')),
            launch_arguments={
                'paused': 'false',
                'use_sim_time': 'true'
            }.items()
        ),

        # Carica il file URDF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': open(os.path.join(tm_description_path, 'urdf', 'tm900_robot_prova2.urdf')).read(),
                'use_sim_time': True
            }]
        ),

        # Carica il file di configurazione dei controller
        Node(
            package='controller_manager',
            executable='spawner',
            name='controller_spawner',
            output='screen',
            arguments=['joint_trajectory_controller']
        ),

        # Spawna il robot in Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_tm5_900',
            output='screen',
            arguments=['-entity', 'tm900', '-topic', 'robot_description']
        )
    ])
