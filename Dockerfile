# ROS 2 Jazzy + Gazebo Harmonic with this cookbook pre-built.
#
#   docker build -t ros2gazebo-cookbook .
#   docker run --rm -it ros2gazebo-cookbook
#   # then, inside: ros2 launch rgc_reference_robot reference_robot.launch.py headless:=true
#
# For GUI (Gazebo/RViz) on Linux/X11, also pass:
#   -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --net=host
FROM osrf/ros:jazzy-desktop

# Gazebo Harmonic (via ros_gz) + keyboard teleop.
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ros-jazzy-ros-gz \
        ros-jazzy-teleop-twist-keyboard \
    && rm -rf /var/lib/apt/lists/*

# Build the cookbook workspace.
WORKDIR /ws
COPY . /ws
RUN . /opt/ros/jazzy/setup.sh \
    && colcon build --event-handlers console_direct+ \
    && chmod +x /ws/docker/entrypoint.sh

ENTRYPOINT ["/ws/docker/entrypoint.sh"]
CMD ["bash"]
