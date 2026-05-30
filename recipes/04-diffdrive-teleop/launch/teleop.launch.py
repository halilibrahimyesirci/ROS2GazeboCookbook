"""Convenience launcher that opens keyboard teleop in its own xterm window.

`teleop_twist_keyboard` needs a real terminal (TTY) to read keystrokes, so this
wraps it with `xterm -e`. Requires xterm to be installed (`sudo apt install
xterm`). If you would rather not use xterm, just run this in a second terminal:

    ros2 run teleop_twist_keyboard teleop_twist_keyboard

Either way it publishes geometry_msgs/msg/Twist on /cmd_vel, which the bridge
forwards to the diff-drive plugin.
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            name='teleop_twist_keyboard',
            prefix='xterm -e',
            output='screen',
        ),
    ])
