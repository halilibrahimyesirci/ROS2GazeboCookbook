# 10 — SLAM

**Verified by CI on:** Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic (gz-sim 8) · `ros_gz` · `slam_toolbox`

Build a map of the world with [`slam_toolbox`](https://github.com/SteveMacenski/slam_toolbox)
while driving the [reference robot](../reference-robot/) around. This recipe
reuses the reference robot and just adds SLAM on top.

## Run it

Terminal 1 — sim + SLAM (+ RViz):

```bash
# from the repo root, after `colcon build` and `source install/setup.bash`
ros2 launch rgc_slam slam.launch.py
```

Terminal 2 — drive the robot to explore and build the map:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Save the finished map:

```bash
ros2 run nav2_map_server map_saver_cli -f my_map
```

## What you should see

In RViz (fixed frame `map`): an occupancy grid that fills in as you drive, the
live LiDAR scan, and the `map → odom → base_link` TF chain.

<!-- When recorded, embed the demo here: docs/media/10-slam.gif -->
> No demo GIF yet — see [docs/media/RECORDING.md](../../docs/media/RECORDING.md) for the exact commands to record one.

## Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/map` | `nav_msgs/msg/OccupancyGrid` | slam_toolbox → ROS |
| `/scan` | `sensor_msgs/msg/LaserScan` | Gazebo → ROS |
| `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo → ROS |

`slam_toolbox` also publishes the `map → odom` transform.

## How it works

- The launch file includes the reference robot (sim + LiDAR + `odom → base_link`
  TF) and adds the `slam_toolbox` async node.
- `config/slam_params.yaml` points SLAM at the robot's frames (`odom`,
  `base_link`) and `/scan`, in `mapping` mode, on sim time.
- As the robot moves, slam_toolbox matches scans, grows the map, and publishes
  the `map → odom` correction.

## Headless / CI

```bash
ros2 launch rgc_slam slam.launch.py headless:=true
```

CI asserts `/map`, `/scan` and `/clock` appear (slam_toolbox is installed in the
CI image), and best-effort checks that a real `/map` is published.

## Troubleshooting

- **No map / empty map** — drive the robot so scans change; SLAM needs motion.
  Check `/scan` has data and TF `odom → base_link` exists.
- **TF errors** — make sure everything is on `use_sim_time:=true` and `/clock` is
  bridged; frame names must be `map`, `odom`, `base_link`.
