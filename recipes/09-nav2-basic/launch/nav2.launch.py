"""Nav2 driving the reference robot to a goal, with slam_toolbox for the map.

One command (then send a goal in RViz — see the README):

    ros2 launch rgc_nav2_basic nav2.launch.py

Headless (no GUI/RViz, used by CI):

    ros2 launch rgc_nav2_basic nav2.launch.py headless:=true
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
    pkg = get_package_share_directory('rgc_nav2_basic')
    slam_pkg = get_package_share_directory('rgc_slam')
    nav2_bringup = get_package_share_directory('nav2_bringup')
    nav2_params = os.path.join(pkg, 'config', 'nav2_params.yaml')
    rviz_config = os.path.join(pkg, 'rviz', 'nav2.rviz')

    headless = LaunchConfiguration('headless').perform(context)
    use_rviz = LaunchConfiguration('rviz').perform(context) == 'true'

    # Reuse recipe 10: reference robot (sim + sensors + bridges) + slam_toolbox,
    # which provides the map and the map -> odom transform Nav2 needs.
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_pkg, 'launch', 'slam.launch.py')),
        launch_arguments={'headless': headless, 'rviz': 'false'}.items(),
    )

    # The Nav2 stack (controller, planner, behaviors, bt_navigator, costmaps),
    # brought up and auto-activated by its lifecycle manager.
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup, 'launch', 'navigation_launch.py')),
        launch_arguments={
            'use_sim_time': 'true',
            'autostart': 'true',
            'params_file': nav2_params,
        }.items(),
    )

    nodes = [slam, nav2]

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
