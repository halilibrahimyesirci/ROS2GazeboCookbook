"""Diff-drive robot + IMU in Gazebo, with odometry/TF/IMU bridged to ROS 2.

One command (then drive it from a second terminal, see the README):

    ros2 launch rgc_diffdrive_teleop diffdrive.launch.py

Headless (no GUI/RViz, used by CI):

    ros2 launch rgc_diffdrive_teleop diffdrive.launch.py headless:=true
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
    pkg = get_package_share_directory('rgc_diffdrive_teleop')
    world = os.path.join(pkg, 'worlds', 'diffdrive_world.sdf')
    model = os.path.join(pkg, 'models', 'diffbot', 'model.sdf')
    bridge_config = os.path.join(pkg, 'config', 'diffdrive_bridge.yaml')
    rviz_config = os.path.join(pkg, 'rviz', 'diffdrive.rviz')

    headless = LaunchConfiguration('headless').perform(context) == 'true'
    use_rviz = LaunchConfiguration('rviz').perform(context) == 'true'

    # Only an IMU here (no rendered camera/lidar), so no render engine is needed
    # even headless: plain '-s -r' is enough.
    gz_args = f'-s -r {world}' if headless else f'-r {world}'

    ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': gz_args,
            'on_exit_shutdown': 'true',
        }.items(),
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-file', model, '-name', 'diffbot', '-z', '0.1'],
        output='screen',
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_config, 'use_sim_time': True}],
        output='screen',
    )

    nodes = [gz_sim, spawn, bridge]

    if use_rviz and not headless:
        nodes.append(Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': True}],
            output='screen',
        ))

    return nodes


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'headless', default_value='false',
            description='Run Gazebo server-only (no GUI), for CI/headless use.'),
        DeclareLaunchArgument(
            'rviz', default_value='true',
            description='Launch RViz2 (ignored when headless:=true).'),
        OpaqueFunction(function=launch_setup),
    ])
