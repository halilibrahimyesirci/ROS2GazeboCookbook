"""Bring up the reference robot: diff-drive base + camera + LiDAR + IMU, bridged.

One command (drive it from a second terminal — see the README):

    ros2 launch rgc_reference_robot reference_robot.launch.py

Headless (no GUI/RViz, used by CI):

    ros2 launch rgc_reference_robot reference_robot.launch.py headless:=true
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
    pkg = get_package_share_directory('rgc_reference_robot')
    world = os.path.join(pkg, 'worlds', 'reference_world.sdf')
    model = os.path.join(pkg, 'models', 'reference_robot', 'model.sdf')
    bridge_config = os.path.join(pkg, 'config', 'reference_bridge.yaml')
    rviz_config = os.path.join(pkg, 'rviz', 'reference.rviz')

    headless = LaunchConfiguration('headless').perform(context) == 'true'
    use_rviz = LaunchConfiguration('rviz').perform(context) == 'true'

    # Camera + LiDAR render, so headless still needs EGL rendering.
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

    spawn = Node(
        package='ros_gz_sim', executable='create',
        arguments=['-file', model, '-name', 'reference_robot', '-z', '0.1'],
        output='screen',
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

    # Sensor frames hang off base_link (the diff-drive plugin gives odom -> base_link).
    tf_camera = Node(
        package='tf2_ros', executable='static_transform_publisher',
        arguments=['--x', '0.22', '--z', '0.05',
                   '--frame-id', 'base_link', '--child-frame-id', 'camera_link'],
        output='screen',
    )
    tf_lidar = Node(
        package='tf2_ros', executable='static_transform_publisher',
        arguments=['--z', '0.18',
                   '--frame-id', 'base_link', '--child-frame-id', 'laser_frame'],
        output='screen',
    )

    nodes = [gz_sim, spawn, image_bridge, param_bridge, tf_camera, tf_lidar]

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
