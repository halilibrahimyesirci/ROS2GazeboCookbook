# Migration kit — Gazebo Classic → new Gazebo

Gazebo Classic reached end-of-life in January 2025. If you are moving a ROS 2
project from **Gazebo Classic + `gazebo_ros_pkgs`** to the **new Gazebo
(`gz-sim`) + `ros_gz`**, start here.

- **[cheatsheet.md](cheatsheet.md)** — the mapping: package names, launch/spawn,
  plugins → systems, SDF changes, and message types, with before/after snippets.
- **[common-errors.md](common-errors.md)** — the errors people actually hit when
  migrating, and how to fix each one.

The big mental shift: in Classic, `gazebo_ros` **plugins inside your model
published ROS topics directly**. In the new Gazebo, the simulator publishes on
**`gz` topics** and you bridge the ones you want into ROS with
[`ros_gz_bridge`](https://github.com/gazebosim/ros_gz). Sensors and controllers
are provided by **gz-sim systems**, not `libgazebo_ros_*` plugins.

Every recipe in this cookbook is already written the new way — use them as
worked examples.
