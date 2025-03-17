from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Percorso al file URDF nel package tm_description
    tm_description_share = get_package_share_directory('tm_description')
    urdf_path = os.path.join(tm_description_share, 'urdf', 'tm900_robot_moveit.urdf')

    # Configura MoveIt per usare questo URDF
    moveit_config = (
        MoveItConfigsBuilder(robot_name="tm900", package_name="moveit_config_tm5_900")
        .robot_description(file_path=urdf_path)   # <--- Aggiunto riferimento al file URDF
        .to_moveit_configs()
    )

    return generate_demo_launch(moveit_config)
