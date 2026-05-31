#!/usr/bin/env bash
# Source ROS and the cookbook overlay, then run whatever command was passed.
set -e
source /opt/ros/jazzy/setup.bash
if [ -f /ws/install/setup.bash ]; then
  source /ws/install/setup.bash
fi
exec "$@"
