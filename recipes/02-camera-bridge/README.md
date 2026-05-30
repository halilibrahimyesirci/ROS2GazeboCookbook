# 02 — Camera bridge

**Verified by CI on:** Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic (gz-sim 8) · `ros_gz` (binary)

Render a camera in Gazebo and stream it into ROS 2 as a `sensor_msgs/msg/Image`,
then view it in RViz. Shows the difference between `ros_gz_image image_bridge`
(for images) and `ros_gz_bridge parameter_bridge` (for everything else).

## Run it

```bash
# from the repo root, after `colcon build` and `source install/setup.bash`
ros2 launch rgc_camera_bridge camera_bridge.launch.py
```

RViz opens with a live camera feed of a red box. You can also use rqt:

```bash
ros2 run rqt_image_view rqt_image_view /camera
```

## What you should see

A 640×480 image of a red box on a grey ground plane.

<!-- When recorded, embed the demo here: docs/media/02-camera-bridge.gif -->
> No demo GIF yet — see [docs/media/RECORDING.md](../../docs/media/RECORDING.md) for the exact commands to record one.

## Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/camera` | `sensor_msgs/msg/Image` | Gazebo → ROS |
| `/camera_info` | `sensor_msgs/msg/CameraInfo` | Gazebo → ROS |
| `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo → ROS |

## How it works

- `worlds/camera_world.sdf` adds the `gz-sim-sensors-system` (with the `ogre2`
  render engine) — **this system is what actually renders sensor data**. A static
  `camera_link` carries a `<sensor type="camera">` publishing on the gz topic
  `camera`.
- `image_bridge camera` republishes the gz image as ROS `/camera`.
- `parameter_bridge` (see `config/camera_bridge.yaml`) bridges `/camera_info` and
  `/clock`. The `frame_id: camera_link` key stamps the camera_info with a frame
  that matches the TF we publish, so RViz is happy.
- A `static_transform_publisher` provides `world → camera_link` so RViz has a
  fixed frame.

## Headless / CI

```bash
ros2 launch rgc_camera_bridge camera_bridge.launch.py headless:=true
```

Adds `--headless-rendering` so the camera still renders (via EGL) without a
display. CI launches this and asserts `/camera`, `/camera_info` and `/clock`
appear; it also best-effort checks that a real frame arrives on `/camera`.

## Troubleshooting

- **Black or empty image** — usually a rendering problem. On a headless box, make
  sure `--headless-rendering` is used and Mesa/EGL is installed; locally, try
  `--render-engine ogre` if `ogre2` misbehaves on your GPU/driver.
- **`/camera` exists but no data** — the `gz-sim-sensors-system` is missing from
  the world, or the world is paused (use `-r`).
- **RViz "Fixed Frame world does not exist"** — the `static_transform_publisher`
  did not start; check the launch output.
