"""SLAM with slam_toolbox on the reference robot.

One command (then drive the robot to build the map — see the README):

    ros2 launch rgc_slam slam.launch.py

Headless (no GUI/RViz, used by CI):

    ros2 launch rgc_slam slam.launch.py headless:=true
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
    pkg = get_package_share_directory('rgc_slam')
    ref = get_package_share_directory('rgc_reference_robot')
    slam_params = os.path.join(pkg, 'config', 'slam_params.yaml')
    rviz_config = os.path.join(pkg, 'rviz', 'slam.rviz')

    headless = LaunchConfiguration('headless').perform(context)
    use_rviz = LaunchConfiguration('rviz').perform(context) == 'true'

    # Reuse the reference robot (sim + sensors + bridges); we add SLAM on top.
    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ref, 'launch', 'reference_robot.launch.py')),
        launch_arguments={'headless': headless, 'rviz': 'false'}.items(),
    )

    # slam_toolbox is a lifecycle node; its own launch file emits the
    # configure -> activate transitions (autostart=true), which is what makes
    # /map appear. Running the bare node would leave it unconfigured.
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('slam_toolbox'),
                         'launch', 'online_async_launch.py')),
        launch_arguments={
            'use_sim_time': 'true',
            'slam_params_file': slam_params,
        }.items(),
    )

    nodes = [sim, slam]

    if use_rviz and headless != 'true':
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
