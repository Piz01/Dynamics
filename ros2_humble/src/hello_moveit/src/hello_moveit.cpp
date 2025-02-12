#include <memory>

#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>

#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <tf2/LinearMath/Quaternion.h>


int main(int argc, char * argv[])
{
  // Initialize ROS and create the Node
  rclcpp::init(argc, argv);
  auto const node = std::make_shared<rclcpp::Node>(
    "hello_moveit",
    rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true)
  );

  // Create a ROS logger
  auto const logger = rclcpp::get_logger("hello_moveit");

  // Next step goes here
  // Create the MoveIt MoveGroup Interface
  moveit::planning_interface::MoveGroupInterface MoveGroupInterface(node, "manipulator");

  tf2::Quaternion tf2_quat;
  tf2_quat.setRPY(0, 0, -3.14/2);
  geometry_msgs::msg::Quaternion msg_quat = tf2::toMsg(tf2_quat);

  geometry_msgs::msg::Pose GoalPose;
  GoalPose.orientation = msg_quat;
  GoalPose.position.x = 0.3;
  GoalPose.position.y = -0.3;
  GoalPose.position.z = 0.4;

  MoveGroupInterface.setPoseTarget(GoalPose);

  moveit::planning_interface::MoveGroupInterface::Plan plan1;
  auto const outcome = static_cast<bool>(MoveGroupInterface.plan(plan1));

  if(outcome)
  {
    MoveGroupInterface.execute(plan1);
  }
  else
  {
    RCLCPP_ERROR(logger, "Errore, movimento non riuscito!");
  }
  
  // Shutdown ROS
  rclcpp::shutdown();
  return 0;
}
