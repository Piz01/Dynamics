cmake_minimum_required(VERSION 3.22)
project(tm_moveit_config)

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)

install(
  PROGRAMS
  launch/demo.launch.py
  scripts/move_robot.py  # Assicurati che il percorso sia corretto
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()

install(DIRECTORY launch DESTINATION share/${PROJECT_NAME}
  PATTERN "setup_assistant.launch" EXCLUDE)
install(DIRECTORY config DESTINATION share/${PROJECT_NAME})
install(FILES .setup_assistant DESTINATION share/${PROJECT_NAME})
