from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_spawn_controllers_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("tm900", package_name="moveit_config_tm5_900").to_moveit_configs()
    return generate_spawn_controllers_launch(moveit_config)
