""" """ """ import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Percorsi dei package
    gazebo_ros_share = get_package_share_directory('gazebo_ros')
    tm_description_share = get_package_share_directory('tm_description')
    tm_moveit_config_share = get_package_share_directory('tm_moveit_config')
    
    # Percorso del file URDF
    urdf_file = os.path.join(tm_description_share, 'urdf', 'tm900_robot_prova2.urdf')
    # Percorso del file di configurazione dei controller
    controllers_yaml = os.path.join(tm_description_share, 'config', 'ros2_controllers.yaml')

    return LaunchDescription([
        # Avvia un world vuoto di Gazebo (usando il file di launch fornito da gazebo_ros)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(tm_moveit_config_share, 'launch', 'empty_world.launch.py')),
            launch_arguments={'paused': 'false', 'use_sim_time': 'true'}.items()
        ),

        # Avvia robot_state_publisher con il robot_description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': open(urdf_file).read(),
                'use_sim_time': True
            }]
        ),

        # Carica i parametri del controller manager
        Node(
            package='controller_manager',
            executable='spawner',
            name='controller_spawner',
            arguments=['joint_trajectory_controller', '--controller-manager', '/controller_manager'],
            output='screen'
        ),

        # Spawna il robot in Gazebo utilizzando il nodo spawn_entity.py
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_tm5_900',
            output='screen',
            arguments=['-entity', 'tm900', '-topic', 'robot_description']
        )
    ])
 """ """
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Ottieni i percorsi dei package
    gazebo_ros_share = get_package_share_directory('gazebo_ros')
    tm_description_share = get_package_share_directory('tm_description')

    # Percorso del file URDF
    urdf_file = os.path.join(tm_description_share, 'urdf', 'tm900_robot_prova2.urdf')
    # Percorso del file di configurazione dei controller
    controllers_yaml = os.path.join(tm_description_share, 'config', 'ros2_controllers.yaml')

    # Leggi il contenuto del file URDF
    if not os.path.exists(urdf_file):
        raise FileNotFoundError(f"File URDF non trovato: {urdf_file}")
    with open(urdf_file, 'r') as infp:
        robot_description_content = infp.read()

    # Nodo: avvio di Gazebo con un world vuoto
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world': os.path.join(gazebo_ros_share, 'worlds', 'empty.world'),
            'paused': 'false',
            'use_sim_time': 'true'
        }.items()
    )

    # Nodo: robot_state_publisher (invia il contenuto del URDF)
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': True
        }]
    )

    # Nodo: gazebo_ros2_control (carica il file YAML dei controller)
    gazebo_ros2_control_node = Node(
        package='gazebo_ros2_control',
        executable='gazebo_ros2_control_node',
        name='gazebo_ros2_control_node',
        output='screen',
        parameters=[controllers_yaml, {'use_sim_time': True}]
    )

    # Nodo: controller spawner (avvia il controller "manipulator_controller" definito nel YAML)
    controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        name='controller_spawner',
        output='screen',
        arguments=['manipulator_controller']  # Assicurati che il nome corrisponda al YAML
    )

    # Il controller_spawner viene lanciato con un ritardo per garantire che gazebo_ros2_control sia attivo
    delayed_controller_spawner = TimerAction(
        period=5.0,
        actions=[controller_spawner]
    )

    return LaunchDescription([
        gazebo,
        rsp_node,
        gazebo_ros2_control_node,
        delayed_controller_spawner,
    ])
 """

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Percorso del file ros2_controllers.yaml
    ros2_controllers_path = os.path.join(
        get_package_share_directory('tm_moveit_config'),
        'config',
        'ros2_controllers.yaml'
    )

    # Avvio di Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={
            'extra_gazebo_args': '--ros-args --params-file ' + ros2_controllers_path
        }.items(),
    )

    # Node per robot_state_publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': LaunchConfiguration('robot_description')
        }]
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher
    ])
