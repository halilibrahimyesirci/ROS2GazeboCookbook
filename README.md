# ROS 2 + Gazebo Cookbook

> Minimal, copy-paste-able, **actually-working** recipes for modern ROS 2 and the
> new Gazebo. Clone it, run one command, and it works in about five minutes.

[![CI](https://github.com/halilibrahimyesirci/ROS2GazeboCookbook/actions/workflows/ci.yml/badge.svg)](https://github.com/halilibrahimyesirci/ROS2GazeboCookbook/actions/workflows/ci.yml)
[![Lint](https://github.com/halilibrahimyesirci/ROS2GazeboCookbook/actions/workflows/lint.yml/badge.svg)](https://github.com/halilibrahimyesirci/ROS2GazeboCookbook/actions/workflows/lint.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ROS 2 Jazzy](https://img.shields.io/badge/ROS%202-Jazzy-22314E?logo=ros&logoColor=white)](https://docs.ros.org/en/jazzy/)
[![Gazebo Harmonic](https://img.shields.io/badge/Gazebo-Harmonic-FB6A2F)](https://gazebosim.org/docs/harmonic/)
[![Ubuntu 24.04](https://img.shields.io/badge/Ubuntu-24.04-E95420?logo=ubuntu&logoColor=white)](https://releases.ubuntu.com/24.04/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## Why this exists

Gazebo Classic reached end-of-life (Jan 2025) and ROS 1 followed (May 2025),
moving the community onto ROS 2 + the new Gazebo (`gz-sim` / `ros_gz`). Working,
up-to-date examples for this stack are still scarce, and most search results
point at outdated ROS 1 + Gazebo Classic material. This repo is a small set of
single-purpose recipes that each solve one common task — and are verified in CI
so they keep working. Full rationale and plan: [ROADMAP.md](ROADMAP.md).

## Recipes

| # | Recipe | What you get | One command | Status |
|---|--------|--------------|-------------|--------|
| 00 | [setup](recipes/00-setup/) | install & verify the whole stack | _(guide)_ | 📘 guide |
| 01 | [spawn-robot](recipes/01-spawn-robot/) | a model in an empty world | `ros2 launch rgc_spawn_robot spawn_robot.launch.py` | 🟢 code + CI |
| 02 | [camera-bridge](recipes/02-camera-bridge/) | camera → ROS image, in RViz | `ros2 launch rgc_camera_bridge camera_bridge.launch.py` | 🟢 code + CI |
| 03 | [lidar-bridge](recipes/03-lidar-bridge/) | 2D LiDAR → ROS, in RViz | `ros2 launch rgc_lidar_bridge lidar_bridge.launch.py` | 🟢 code + CI |
| 04 | [diffdrive-teleop](recipes/04-diffdrive-teleop/) | drive a robot; IMU + odom + TF | `ros2 launch rgc_diffdrive_teleop diffdrive.launch.py` | 🟢 code + CI |
| 05 | [custom-world](recipes/05-custom-world/) | a walled arena: lights, materials, obstacles | `ros2 launch rgc_custom_world custom_world.launch.py` | 🟢 code + CI |
| 07 | [multiple-sensors](recipes/07-multiple-sensors/) | camera + LiDAR + IMU on one robot | `ros2 launch rgc_multiple_sensors multiple_sensors.launch.py` | 🟢 code + CI |

`🟢 code + CI` = builds, launches headless, and the expected ROS topics are
asserted in CI. Demo GIFs are not recorded yet (see
[docs/media/RECORDING.md](docs/media/RECORDING.md)); a recipe is only marked
"done" once it also has one.

## Target stack

| Component | Version |
|-----------|---------|
| OS | Ubuntu 24.04 |
| ROS 2 | Jazzy Jalisco (LTS) |
| Gazebo | Harmonic (gz-sim 8, LTS) |
| Bridge | `ros_gz` (`ros_gz_sim`, `ros_gz_bridge`, `ros_gz_image`) |

## Quick start

```bash
# 1. Prerequisites (full guide: recipes/00-setup)
sudo apt install -y ros-jazzy-ros-gz ros-jazzy-teleop-twist-keyboard

# 2. Get and build the cookbook
git clone https://github.com/halilibrahimyesirci/ROS2GazeboCookbook.git
cd ROS2GazeboCookbook
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths recipes --ignore-src -r -y
colcon build
source install/setup.bash

# 3. Run a recipe
ros2 launch rgc_spawn_robot spawn_robot.launch.py
```

New to the stack? Start with [recipes/00-setup](recipes/00-setup/), which also
verifies the bridge end-to-end before you run anything else.

## Repository layout

```text
recipes/
  00-setup/          install + verify guide (docs only)
  01-spawn-robot/    package rgc_spawn_robot
  02-camera-bridge/  package rgc_camera_bridge
  03-lidar-bridge/   package rgc_lidar_bridge
  04-diffdrive-teleop/ package rgc_diffdrive_teleop
tools/               headless smoke-test scripts used by CI
docs/media/          demo GIFs (+ RECORDING.md guide)
.github/workflows/   CI (build + headless smoke) and lint
```

Each recipe is a self-contained colcon (`ament_cmake`) package with its own
launch file, world/model, bridge config and README. A single `colcon build` at
the repo root builds them all.

## How CI verifies recipes

Every push runs the recipes on a clean Ubuntu 24.04 + ROS 2 Jazzy + Gazebo
Harmonic container. For each recipe, CI builds the workspace, launches it
**headless** (camera/LiDAR render off-screen via EGL), and asserts the expected
ROS topics appear. It also does a *best-effort* check that real sensor data
flows — that check is allowed to be flaky, because GPU-less software rendering in
CI is not 100% reliable, so it never fails the build.

In other words: a green CI badge means **builds + launches + expected topics
present**. That is exactly what it claims — nothing more. See
[.github/workflows/ci.yml](.github/workflows/ci.yml).

## Contributing

Issues and PRs are welcome — new recipes, fixes, and "this broke on distro X"
reports. The bar for a recipe is simple: it runs from a clean install with one
command, has a short README, and states the versions it was tested on. See
[CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).
Security reports: [SECURITY.md](SECURITY.md).

## License & citation

MIT — see [LICENSE](LICENSE). If you reference this work, a
[CITATION.cff](CITATION.cff) is provided.

## Author

**Halil İbrahim Yesirci** — [@halilibrahimyesirci](https://github.com/halilibrahimyesirci)
