# Reference robot

**Verified by CI on:** Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic (gz-sim 8) · `ros_gz` (binary)

One clean diff-drive robot that carries a camera, a 2D LiDAR and an IMU, with
teleop and every topic bridged. This is the platform the navigation recipes
(Nav2, SLAM) build on — it ties the earlier recipes together.

## Run it

Terminal 1 — bring up the robot (+ RViz):

```bash
# from the repo root, after `colcon build` and `source install/setup.bash`
ros2 launch rgc_reference_robot reference_robot.launch.py
```

Terminal 2 — drive it:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

## What you should see

The robot driving among pillars and a wall in Gazebo, while RViz shows the
camera image, the LiDAR scan, the odometry trail and the full TF tree
(`odom → base_link → camera_link / laser_frame`).

<!-- When recorded, embed the demo here: docs/media/reference-robot.gif -->
> No demo GIF yet — see [docs/media/RECORDING.md](../../docs/media/RECORDING.md) for the exact commands to record one.

## Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | ROS → Gazebo |
| `/odom` | `nav_msgs/msg/Odometry` | Gazebo → ROS |
| `/tf` | `tf2_msgs/msg/TFMessage` | Gazebo → ROS |
| `/scan` | `sensor_msgs/msg/LaserScan` | Gazebo → ROS |
| `/imu` | `sensor_msgs/msg/Imu` | Gazebo → ROS |
| `/camera` + `/camera_info` | `sensor_msgs/msg/Image` + `CameraInfo` | Gazebo → ROS |
| `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo → ROS |

## How it works

- `models/reference_robot/model.sdf` is the recipe-04 diff-drive base with a
  camera, a `gpu_lidar` and an IMU added on `base_link`.
- `worlds/reference_world.sdf` loads the `sensors-system` and `imu-system` and
  gives the robot some pillars and a wall to drive around.
- `config/reference_bridge.yaml` bridges everything in one file; the launch adds
  `image_bridge` for the image and the `base_link → camera_link` /
  `base_link → laser_frame` static transforms. The diff-drive plugin supplies
  `odom → base_link`, so the TF tree is complete with `odom` as the fixed frame.

## Headless / CI

```bash
ros2 launch rgc_reference_robot reference_robot.launch.py headless:=true
```

CI asserts `/cmd_vel`, `/odom`, `/tf`, `/scan`, `/imu`, `/camera` and `/clock`
appear, and best-effort checks real scan data on `/scan`.

## Troubleshooting

- **Robot does not move** — confirm `/cmd_vel` reaches the diff-drive plugin
  (`ros2 topic echo /odom` should change as you publish).
- **A sensor frame is missing in RViz** — a static transform did not start, or
  the fixed frame is not `odom`.
