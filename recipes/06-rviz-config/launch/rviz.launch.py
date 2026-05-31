"""Open RViz with a ready-made config from this package.

Pick a config with the `config` argument (file name without `.rviz`):

    ros2 launch rgc_rviz_config rviz.launch.py config:=combined
    ros2 launch rgc_rviz_config rviz.launch.py config:=tf_only

Run it alongside a sim recipe started with rviz:=false, e.g.:

    ros2 launch rgc_multiple_sensors multiple_sensors.launch.py rviz:=false
    ros2 launch rgc_rviz_config rviz.launch.py config:=combined
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    pkg = get_package_share_directory('rgc_rviz_config')
    config_name = LaunchConfiguration('config').perform(context)
    use_sim_time = LaunchConfiguration('use_sim_time').perform(context) == 'true'
    rviz_config = os.path.join(pkg, 'rviz', f'{config_name}.rviz')

    return [Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen',
    )]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'config', default_value='combined',
            description='RViz config to open (file name without .rviz): combined | tf_only'),
        DeclareLaunchArgument(
            'use_sim_time', default_value='true',
            description='Use simulation time to match a running sim.'),
        OpaqueFunction(function=launch_setup),
    ])
