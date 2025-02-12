import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/pizzu01/ros2_humble/install/ros_tcp_endpoint'
