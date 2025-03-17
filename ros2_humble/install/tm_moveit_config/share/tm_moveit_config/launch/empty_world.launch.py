from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # Avvia Gazebo in un world vuoto
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '--pause', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),

        # Avvia robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': True}]
        )
    ])

