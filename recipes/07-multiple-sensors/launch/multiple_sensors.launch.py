"""One robot, three sensors (camera + LiDAR + IMU), all bridged into ROS 2.

One command:

    ros2 launch rgc_multiple_sensors multiple_sensors.launch.py

Headless (no GUI/RViz, used by CI):

    ros2 launch rgc_multiple_sensors multiple_sensors.launch.py headless:=true
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    pkg = get_package_share_directory('rgc_multiple_sensors')
    world = os.path.join(pkg, 'worlds', 'sensors_world.sdf')
    bridge_config = os.path.join(pkg, 'config', 'sensors_bridge.yaml')
    rviz_config = os.path.join(pkg, 'rviz', 'sensors.rviz')

    headless = LaunchConfiguration('headless').perform(context) == 'true'
    use_rviz = LaunchConfiguration('rviz').perform(context) == 'true'

    # Camera + LiDAR are rendered sensors, so headless still needs EGL rendering.
    if headless:
        gz_args = f'-s -r --headless-rendering {world}'
    else:
        gz_args = f'-r {world}'

    ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': gz_args, 'on_exit_shutdown': 'true'}.items(),
    )

    image_bridge = Node(
        package='ros_gz_image', executable='image_bridge',
        arguments=['camera'], output='screen',
    )

    param_bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge',
        parameters=[{'config_file': bridge_config, 'use_sim_time': True}],
        output='screen',
    )

    # The three sensor frames hang off base_link (matching the SDF mount poses).
    tf_camera = Node(
        package='tf2_ros', executable='static_transform_publisher',
        arguments=['--x', '0.16', '--frame-id', 'base_link', '--child-frame-id', 'camera_link'],
        output='screen',
    )
    tf_lidar = Node(
        package='tf2_ros', executable='static_transform_publisher',
        arguments=['--z', '0.15', '--frame-id', 'base_link', '--child-frame-id', 'laser_frame'],
        output='screen',
    )

    nodes = [gz_sim, image_bridge, param_bridge, tf_camera, tf_lidar]

    if use_rviz and not headless:
        nodes.append(Node(
            package='rviz2', executable='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': True}],
            output='screen',
        ))

    return nodes


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'headless', default_value='false',
            description='Run Gazebo server-only with EGL headless rendering (CI).'),
        DeclareLaunchArgument(
            'rviz', default_value='true',
            description='Launch RViz2 (ignored when headless:=true).'),
        OpaqueFunction(function=launch_setup),
    ])
