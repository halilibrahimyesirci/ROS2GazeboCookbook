# Migration cheatsheet — Classic → new Gazebo

Quick reference for moving a ROS 2 project from **Gazebo Classic +
`gazebo_ros_pkgs`** to **new Gazebo (`gz-sim`) + `ros_gz`** (this cookbook
targets ROS 2 Jazzy + Gazebo Harmonic).

## Names & packages

| Classic | New Gazebo |
|---------|-----------|
| `gazebo` / `gzserver` / `gzclient` | `gz sim` |
| `gazebo_ros`, `gazebo_ros_pkgs` | `ros_gz` (`ros_gz_sim`, `ros_gz_bridge`, `ros_gz_image`) |
| `gazebo_ros` `gazebo.launch.py` | `ros_gz_sim` `gz_sim.launch.py` |
| `spawn_entity.py` | `ros_gz_sim` `create` |
| `ignition` / `ign` (Fortress and older) | `gz` (Garden onward) |

Install: `sudo apt install ros-jazzy-ros-gz` (pulls Gazebo Harmonic as a vendor
package — no separate Gazebo apt source needed on Jazzy).

## Launch & spawn

```diff
- # Classic
- ros2 launch gazebo_ros gazebo.launch.py world:=my.world
- ros2 run gazebo_ros spawn_entity.py -topic robot_description -entity robot
+ # New Gazebo
+ ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="-r my.sdf"
+ ros2 run ros_gz_sim create -topic robot_description -name robot
```

## The big difference: plugins → systems + bridge

In Classic, `libgazebo_ros_*` plugins inside the model published ROS topics
directly. In new Gazebo, **gz-sim systems** produce data on **gz topics**, and
you bridge what you want with `ros_gz_bridge`.

| Classic plugin (`libgazebo_ros_*`) | New Gazebo system | Then bridge |
|------------------------------------|-------------------|-------------|
| `libgazebo_ros_camera` | `<sensor type="camera">` + `gz-sim-sensors-system` | `ros_gz_image image_bridge` (+ `camera_info` via `ros_gz_bridge`) |
| `libgazebo_ros_ray_sensor` (LiDAR) | `<sensor type="gpu_lidar">` + `gz-sim-sensors-system` | `LaserScan` ↔ `gz.msgs.LaserScan` |
| `libgazebo_ros_imu_sensor` | `<sensor type="imu">` + `gz-sim-imu-system` | `Imu` ↔ `gz.msgs.IMU` |
| `libgazebo_ros_diff_drive` | `gz-sim-diff-drive-system` | `cmd_vel` (ROS→GZ), `odom`, `tf` |
| `libgazebo_ros_joint_state_publisher` | `gz-sim-joint-state-publisher-system` | `JointState` ↔ `gz.msgs.Model` |
| `libgazebo_ros_p3d` (ground-truth pose) | `gz-sim-pose-publisher-system` | `Pose`/`TF` ↔ `gz.msgs.Pose_V` |

**Gotcha:** in a Classic world, default plugins were implicit. In new Gazebo,
**declaring any `<plugin>` disables the auto-loaded defaults**, so every world
must list its systems explicitly — at minimum `gz-sim-physics-system`,
`gz-sim-scene-broadcaster-system` and `gz-sim-user-commands-system` (the last is
needed to spawn).

## SDF changes

- Bump the SDF version (Classic models are often `1.6`; Harmonic uses `1.10`+).
- Plugin element changes from a shared-library reference to a system:
  ```diff
  - <plugin name="diff" filename="libgazebo_ros_diff_drive.so"> ... </plugin>
  + <plugin filename="gz-sim-diff-drive-system" name="gz::sim::systems::DiffDrive"> ... </plugin>
  ```
- Sensor `<topic>` sets the **gz** topic; the ROS topic comes from the bridge.
- For RViz-friendly frames, set the bridged message's `frame_id` in the bridge
  YAML (`frame_id:` key) rather than relying on the scoped gz frame name.

## Message type bridge map

| ROS 2 type | gz type |
|------------|---------|
| `sensor_msgs/msg/Image` | `gz.msgs.Image` |
| `sensor_msgs/msg/CameraInfo` | `gz.msgs.CameraInfo` |
| `sensor_msgs/msg/LaserScan` | `gz.msgs.LaserScan` |
| `sensor_msgs/msg/Imu` | `gz.msgs.IMU` |
| `sensor_msgs/msg/PointCloud2` | `gz.msgs.PointCloudPacked` |
| `nav_msgs/msg/Odometry` | `gz.msgs.Odometry` |
| `geometry_msgs/msg/Twist` | `gz.msgs.Twist` |
| `tf2_msgs/msg/TFMessage` | `gz.msgs.Pose_V` |
| `rosgraph_msgs/msg/Clock` | `gz.msgs.Clock` |

Bridge direction symbols (CLI): `@` bidirectional, `[` GZ→ROS, `]` ROS→GZ. In a
YAML config: `direction: BIDIRECTIONAL | GZ_TO_ROS | ROS_TO_GZ`.

## Sim time

Classic published `/clock` via `gazebo_ros`. In new Gazebo, bridge it yourself
(`/clock` ↔ `gz.msgs.Clock`, GZ→ROS) and run nodes with `use_sim_time:=true`.

## Worked examples

Each cookbook recipe is the "new Gazebo" side of this table:
camera → [02](../recipes/02-camera-bridge/), LiDAR → [03](../recipes/03-lidar-bridge/),
diff-drive + IMU → [04](../recipes/04-diffdrive-teleop/), everything together →
[reference-robot](../recipes/reference-robot/).
