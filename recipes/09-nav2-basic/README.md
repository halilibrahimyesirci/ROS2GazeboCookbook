# 09 — Nav2 basic

**Verified by CI on:** Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic (gz-sim 8) · `ros_gz` · `navigation2` · `slam_toolbox`

Drive the [reference robot](../reference-robot/) to a goal with the **Nav2**
stack. It reuses recipe 10 (reference robot + `slam_toolbox`) for the map and
localization, and adds the Nav2 navigation stack on top.

## Run it

Terminal 1 — sim + SLAM + Nav2 (+ RViz):

```bash
# from the repo root, after `colcon build` and `source install/setup.bash`
ros2 launch rgc_nav2_basic nav2.launch.py
```

In RViz, use the **2D Goal Pose** tool (top toolbar) to click a goal. Nav2 plans
a path and drives the robot there, avoiding the pillars and wall.

## What you should see

In RViz (fixed frame `map`): the SLAM map, the global costmap, the planned path
(green), the live scan, and the robot driving to the goal you click.

<!-- When recorded, embed the demo here: docs/media/09-nav2-basic.gif -->
> No demo GIF yet — see [docs/media/RECORDING.md](../../docs/media/RECORDING.md) for the exact commands to record one.

## Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/global_costmap/costmap` | `nav_msgs/msg/OccupancyGrid` | Nav2 → ROS |
| `/local_costmap/costmap` | `nav_msgs/msg/OccupancyGrid` | Nav2 → ROS |
| `/plan` | `nav_msgs/msg/Path` | Nav2 → ROS |
| `/goal_pose` | `geometry_msgs/msg/PoseStamped` | RViz → Nav2 |
| `/scan`, `/map`, `/clock` | (from the reference robot + SLAM) | Gazebo/SLAM → ROS |

## How it works

- The launch file includes recipe 10's `slam.launch.py` (reference robot + sim +
  `slam_toolbox`), which supplies `/map` and the `map → odom` transform.
- It then includes Nav2's `navigation_launch.py` with
  [`config/nav2_params.yaml`](config/nav2_params.yaml): a RegulatedPurePursuit
  controller, a NavFn planner, a 2D-LiDAR obstacle costmap, and recovery
  behaviors — all auto-activated by Nav2's lifecycle manager.

## Headless / CI

```bash
ros2 launch rgc_nav2_basic nav2.launch.py headless:=true
```

CI asserts the global and local costmaps publish (proving the Nav2 stack came up
and activated), alongside `/scan` and `/clock`.

## Troubleshooting

- **Costmaps never appear** — a Nav2 node failed to configure; check the launch
  output for the first lifecycle error (usually a plugin name or a frame).
- **Robot plans but does not move** — check what topic Nav2's velocity output
  lands on (`ros2 topic list`); the reference robot drives off `/cmd_vel`.
- **"No map received"** — give SLAM a moment, and make sure everything is on
  `use_sim_time:=true`.
