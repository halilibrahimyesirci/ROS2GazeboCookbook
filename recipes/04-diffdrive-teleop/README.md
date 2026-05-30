# 04 — Diff-drive + IMU + teleop

**Verified by CI on:** Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic (gz-sim 8) · `ros_gz` (binary)

A differential-drive robot with an IMU that you drive from the keyboard. This is
the recipe that ties the others together: spawning a model, the diff-drive
plugin, odometry + TF, an IMU, and a two-way bridge (commands in, state out).

## Run it

Terminal 1 — start the sim + bridge (+ RViz):

```bash
# from the repo root, after `colcon build` and `source install/setup.bash`
ros2 launch rgc_diffdrive_teleop diffdrive.launch.py
```

Terminal 2 — drive it:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Use `i` / `,` to go forward/back and `j` / `l` to turn. Watch the robot move in
Gazebo and the odometry/TF update in RViz.

> Prefer one command? `ros2 launch rgc_diffdrive_teleop teleop.launch.py` opens
> teleop in an xterm window (needs `xterm` installed).

## What you should see

The robot drives around two pillars in Gazebo; in RViz the `base_link` frame and
the odometry trail follow it on the `odom` fixed frame.

<!-- When recorded, embed the demo here: docs/media/04-diffdrive-teleop.gif -->
> No demo GIF yet — see [docs/media/RECORDING.md](../../docs/media/RECORDING.md) for the exact commands to record one.

## Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | ROS → Gazebo |
| `/odom` | `nav_msgs/msg/Odometry` | Gazebo → ROS |
| `/tf` | `tf2_msgs/msg/TFMessage` | Gazebo → ROS |
| `/imu` | `sensor_msgs/msg/Imu` | Gazebo → ROS |
| `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo → ROS |

## How it works

- `models/diffbot/model.sdf` is the robot: a chassis, two wheels on revolute
  joints, a frictionless caster, an `<sensor type="imu">`, and the
  `gz-sim-diff-drive-system` plugin. The plugin subscribes to the gz `cmd_vel`
  topic and publishes odometry and the `odom → base_link` TF.
- `worlds/diffdrive_world.sdf` adds the `gz-sim-imu-system` so the IMU produces
  data. There is no rendered sensor, so the world runs fully headless with no
  render engine.
- `config/diffdrive_bridge.yaml` bridges all five topics. Note `/cmd_vel` is the
  only `ROS_TO_GZ` entry — it is how your keyboard reaches the wheels.

## Teleop note

`teleop_twist_keyboard` reads the keyboard, so it needs its own real terminal —
it cannot be a backgrounded launch node. Run it in a second terminal (above), or
use `teleop.launch.py` which wraps it in an xterm. CI skips teleop and only
checks that the sim + bridge come up and publish the expected topics.

## Headless / CI

```bash
ros2 launch rgc_diffdrive_teleop diffdrive.launch.py headless:=true
```

CI asserts `/cmd_vel`, `/odom`, `/tf`, `/imu` and `/clock` appear, and
best-effort checks that real odometry is published on `/odom`.

## Troubleshooting

- **Robot does not move** — confirm `/cmd_vel` is bridged `ROS_TO_GZ` and that the
  plugin's `<topic>` is `cmd_vel`; check `ros2 topic echo /odom` changes when you
  publish a Twist.
- **Robot drifts / tips over** — wheel friction or the caster `mu=0` is wrong, or
  the spawn height (`-z 0.1`) does not match the wheel radius.
- **Jazzy wants TwistStamped** — some stacks default to `TwistStamped`; this recipe
  uses plain `Twist` to match `teleop_twist_keyboard`'s default.
