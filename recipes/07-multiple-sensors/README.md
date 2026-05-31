# 07 — Multiple sensors

**Verified by CI on:** Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic (gz-sim 8) · `ros_gz` (binary)

One robot carrying a camera, a 2D LiDAR and an IMU — all bridged into ROS 2 at
once and shown together in RViz. This is the clean way to combine recipes 02, 03
and 04's sensors on a single platform, with a frame per sensor.

## Run it

```bash
# from the repo root, after `colcon build` and `source install/setup.bash`
ros2 launch rgc_multiple_sensors multiple_sensors.launch.py
```

RViz opens with the camera image, the LiDAR scan and the TF tree all live.

## What you should see

A camera panel (red box ahead), a 360° LaserScan picking out three boxes, and the
`base_link → camera_link` / `base_link → laser_frame` TF frames, on fixed frame
`base_link`.

<!-- When recorded, embed the demo here: docs/media/07-multiple-sensors.gif -->
> No demo GIF yet — see [docs/media/RECORDING.md](../../docs/media/RECORDING.md) for the exact commands to record one.

## Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/camera` | `sensor_msgs/msg/Image` | Gazebo → ROS |
| `/camera_info` | `sensor_msgs/msg/CameraInfo` | Gazebo → ROS |
| `/scan` | `sensor_msgs/msg/LaserScan` | Gazebo → ROS |
| `/imu` | `sensor_msgs/msg/Imu` | Gazebo → ROS |
| `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo → ROS |

## How it works

- `worlds/sensors_world.sdf` puts all three sensors on one `base_link` and loads
  **both** the `gz-sim-sensors-system` (for the camera + LiDAR, which render) and
  the `gz-sim-imu-system` (for the IMU). Each sensor gets a distinct gz topic
  (`camera`, `scan`, `imu`) so nothing collides.
- `image_bridge` carries the image; `parameter_bridge` carries camera_info, scan,
  imu and clock, each with a `frame_id` that matches a published TF frame.
- Two `static_transform_publisher`s give `base_link → camera_link` and
  `base_link → laser_frame`, so RViz lines everything up on one fixed frame.

## Headless / CI

```bash
ros2 launch rgc_multiple_sensors multiple_sensors.launch.py headless:=true
```

CI asserts `/camera`, `/scan`, `/imu` and `/clock` all appear, and best-effort
checks that real scan data arrives on `/scan`.

## Troubleshooting

- **One sensor is missing** — check that its `<topic>` is unique and that the
  world declares the matching system (`sensors-system` for camera/LiDAR,
  `imu-system` for the IMU).
- **RViz frames are off** — the static transform offsets must match the sensor
  `<pose>`s in the SDF.
