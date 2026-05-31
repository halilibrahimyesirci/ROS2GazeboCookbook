"""Load a custom world (walls, lights, obstacles) and spawn a robot into it.

One command:

    ros2 launch rgc_custom_world custom_world.launch.py

Headless (no GUI, used by CI):

    ros2 launch rgc_custom_world custom_world.launch.py headless:=true
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
    pkg = get_package_share_directory('rgc_custom_world')
    world = os.path.join(pkg, 'worlds', 'custom_world.sdf')
    model = os.path.join(pkg, 'models', 'robot', 'model.sdf')
    bridge_config = os.path.join(pkg, 'config', 'clock_bridge.yaml')

    headless = LaunchConfiguration('headless').perform(context) == 'true'
    gz_args = f'-s -r {world}' if headless else f'-r {world}'

    ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': gz_args, 'on_exit_shutdown': 'true'}.items(),
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-file', model, '-name', 'robot', '-x', '0', '-y', '0', '-z', '0.1'],
        output='screen',
    )

    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_config, 'use_sim_time': True}],
        output='screen',
    )

    return [gz_sim, spawn, clock_bridge]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'headless', default_value='false',
            description='Run Gazebo server-only (no GUI), for CI/headless use.'),
        DeclareLaunchArgument(
            'rviz', default_value='false',
            description='Unused in this recipe (kept for a consistent interface).'),
        OpaqueFunction(function=launch_setup),
    ])
