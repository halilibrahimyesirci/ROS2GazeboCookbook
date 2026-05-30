# 03 — LiDAR bridge

**Verified by CI on:** Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic (gz-sim 8) · `ros_gz` (binary)

Bridge a 2D GPU LiDAR from Gazebo into a ROS 2 `sensor_msgs/msg/LaserScan` and
visualize the returns in RViz. Also shows the clean way to give a sensor a frame
RViz can resolve.

## Run it

```bash
# from the repo root, after `colcon build` and `source install/setup.bash`
ros2 launch rgc_lidar_bridge lidar_bridge.launch.py
```

RViz opens and shows a 360° scan with three boxes picked out around the sensor.

## What you should see

A ring of red scan points in RViz with gaps/edges where the three colored boxes
are, on the `base_link` fixed frame.

<!-- When recorded, embed the demo here: docs/media/03-lidar-bridge.gif -->
> No demo GIF yet — see [docs/media/RECORDING.md](../../docs/media/RECORDING.md) for the exact commands to record one.

## Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/scan` | `sensor_msgs/msg/LaserScan` | Gazebo → ROS |
| `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo → ROS |

## How it works

- `worlds/lidar_world.sdf` adds the `gz-sim-sensors-system` (ogre2) and a static
  post carrying a `<sensor type="gpu_lidar">` that publishes on the gz topic
  `scan`. Three boxes give the scan something to return off.
- `parameter_bridge` (see `config/lidar_bridge.yaml`) bridges `/scan` and
  `/clock`. The `frame_id: laser_frame` key sets a clean frame on the LaserScan.
- A `static_transform_publisher` publishes `base_link → laser_frame` (0.3 m up),
  so RViz, with fixed frame `base_link`, can place the scan correctly. This is
  the idiomatic fix for the "sensor data has a frame RViz can't find" problem.

## Headless / CI

```bash
ros2 launch rgc_lidar_bridge lidar_bridge.launch.py headless:=true
```

CI launches this and asserts `/scan` and `/clock` appear, then best-effort checks
that a real `LaserScan` message arrives on `/scan`.

## Troubleshooting

- **Scan is empty / no points in RViz** — set the RViz LaserScan display QoS to
  *Best Effort* (already set in the provided config) and make sure the fixed frame
  is `base_link`.
- **`/scan` exists but no data** — the `gz-sim-sensors-system` is missing, the
  world is paused, or (headless) `--headless-rendering` was not passed.
- **TF error in RViz** — the `static_transform_publisher` did not start.
