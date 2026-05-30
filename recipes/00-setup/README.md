# 00 — Setup & verify

Install the exact stack this cookbook targets and prove the ROS ↔ Gazebo bridge
works before you run any recipe.

**Target stack**

| Component | Version |
|-----------|---------|
| OS | Ubuntu 24.04 (Noble) |
| ROS 2 | Jazzy Jalisco (LTS) |
| Gazebo | Harmonic (gz-sim 8, LTS) |
| Bridge | `ros_gz` (binary, from apt) |

> On Jazzy, the `ros-jazzy-ros-gz` package pulls in **Gazebo Harmonic** for you
> as a ROS vendor package — you do **not** need a separate Gazebo apt source.

## 1. Install ROS 2 Jazzy

Follow the official guide (authoritative, kept up to date):
<https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html>. In short:

```bash
# enable the universe repo and add the ROS 2 apt source
sudo apt update && sudo apt install -y software-properties-common curl
sudo add-apt-repository universe
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest \
  | grep -F '"tag_name"' | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb \
  "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb"
sudo apt install -y /tmp/ros2-apt-source.deb
sudo apt update

# desktop install + build tools
sudo apt install -y ros-jazzy-desktop ros-dev-tools
```

Source ROS in every new shell (or add this to `~/.bashrc`):

```bash
source /opt/ros/jazzy/setup.bash
```

## 2. Install Gazebo Harmonic + the bridge

```bash
sudo apt install -y ros-jazzy-ros-gz ros-jazzy-teleop-twist-keyboard
```

This installs `ros_gz_sim`, `ros_gz_bridge`, `ros_gz_image` and Gazebo Harmonic.
Do **not** also install `gazebo` (that is the end-of-life Gazebo Classic).

## 3. Verify Gazebo

```bash
gz sim --version      # expect Gazebo Sim 8.x (Harmonic)
gz sim -r shapes.sdf  # a window with falling shapes; close it to exit
```

## 4. Verify the bridge end-to-end

Terminal 1 — start an empty world (server only is fine):

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="-r empty.sdf"
```

Terminal 2 — bridge the clock and watch it tick:

```bash
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock
# in a third terminal:
ros2 topic echo /clock
```

Rising timestamps on `/clock` mean the bridge is alive. The `@` selects a
bidirectional bridge; `[` is GZ→ROS only and `]` is ROS→GZ only.

## 5. Build this cookbook

```bash
git clone https://github.com/halilibrahimyesirci/ROS2GazeboCookbook.git
cd ROS2GazeboCookbook
rosdep install --from-paths recipes --ignore-src -r -y
colcon build
source install/setup.bash
```

Now run any recipe, e.g. `ros2 launch rgc_spawn_robot spawn_robot.launch.py`.

## 6. Headless / CI

No display? Render sensors off-screen with EGL:

```bash
DISPLAY= gz sim -v 4 -s -r --headless-rendering empty.sdf
```

This is exactly how CI runs every recipe (`headless:=true`).

## Troubleshooting

- **`gz: command not found`** — `ros-jazzy-ros-gz` is not installed, or you have
  not opened a new shell. The `gz` CLI ships with the Gazebo dependencies it pulls.
- **`Failed to load plugin ... ignition-...`** — you copied an old tutorial.
  Harmonic uses `gz-sim-*-system` / `gz::sim::systems::*`, not `ignition-*`.
- **Black or empty Gazebo window** — GPU/driver issue. Try
  `gz sim --render-engine ogre ...`, or run headless with `--headless-rendering`.
- **Bridge prints nothing** — the gz message type string is wrong (it must be
  `gz.msgs.*`), or the world is paused (start it with `-r`).
- **RViz shows nothing** — wrong *Fixed Frame*, missing TF, or nodes are not on
  sim time. Recipes here set `use_sim_time:=true` and bridge `/clock`.
- **`ros_gz_sim` package not found** — re-source `/opt/ros/jazzy/setup.bash` and
  confirm `ros2 pkg prefix ros_gz_sim` resolves.
