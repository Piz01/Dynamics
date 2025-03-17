from setuptools import find_packages, setup

package_name = 'my_ros2_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pizzu01',
    maintainer_email='pizzu01@todo.todo',
    description='Package per creare un nodo che restituisce la pos di un oggetto di Unity',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [ 'object_position_node = my_ros2_package.object_position_node:main',
				'pose_listener = my_ros2_package.pose_listener:main',
                              'moveit_controller = my_ros2_package.moveit_controller:main',
                              'fake_joint_state_publisher = my_ros2_package.fake_joint_state_publisher:main',
        ],
    },
)
