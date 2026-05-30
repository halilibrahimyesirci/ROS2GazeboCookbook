"""Bridge a Gazebo camera into ROS 2 and show it in RViz.

One command:

    ros2 launch rgc_camera_bridge camera_bridge.launch.py

Headless (no GUI/RViz, used by CI):

    ros2 launch rgc_camera_bridge camera_bridge.launch.py headless:=true
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
    pkg = get_package_share_directory('rgc_camera_bridge')
    world = os.path.join(pkg, 'worlds', 'camera_world.sdf')
    bridge_config = os.path.join(pkg, 'config', 'camera_bridge.yaml')
    rviz_config = os.path.join(pkg, 'rviz', 'camera.rviz')

    headless = LaunchConfiguration('headless').perform(context) == 'true'
    use_rviz = LaunchConfiguration('rviz').perform(context) == 'true'

    # A camera is a rendered sensor, so headless runs still need a render engine.
    # '--headless-rendering' uses EGL to render off-screen with no display.
    if headless:
        gz_args = f'-s -r --headless-rendering {world}'
    else:
        gz_args = f'-r {world}'

    ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': gz_args,
            'on_exit_shutdown': 'true',
        }.items(),
    )

    # image_bridge handles the raw image (and its image_transport variants).
    image_bridge = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['camera'],
        output='screen',
    )

    # parameter_bridge handles camera_info and the clock.
    param_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_config, 'use_sim_time': True}],
        output='screen',
    )

    # Give RViz a frame to anchor to (the camera is static in the world).
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['--frame-id', 'world', '--child-frame-id', 'camera_link'],
        output='screen',
    )

    nodes = [gz_sim, image_bridge, param_bridge, static_tf]

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
            description='Run Gazebo server-only with EGL headless rendering (CI).'),
        DeclareLaunchArgument(
            'rviz', default_value='true',
            description='Launch RViz2 (ignored when headless:=true).'),
        OpaqueFunction(function=launch_setup),
    ])
