# Contributing

Thanks for helping make ROS 2 + Gazebo easier for everyone. New recipes, fixes,
and "this broke on distro X" reports are all welcome.

## The bar for a recipe

A recipe is small and self-contained. Before it merges it should:

1. **Run from a clean install with one command** — `ros2 launch <pkg> <file>`.
2. **Have a short README** in the same shape as the existing recipes (what it
   does, run it, what you should see, topics, how it works, headless/CI,
   troubleshooting).
3. **State the exact versions it was tested on** (ROS distro, Gazebo version, OS).
4. **Accept a `headless:=true` argument** so CI can launch it without a display.
5. **Be wired into CI** — add a row to the matrix in
   [.github/workflows/ci.yml](.github/workflows/ci.yml) with the package name,
   launch file, and the topics CI should assert.

Small and working beats big and broken. Open an issue before a large addition so
we can keep recipes minimal and consistent.

## Dev setup

```bash
git clone https://github.com/halilibrahimyesirci/ROS2GazeboCookbook.git
cd ROS2GazeboCookbook
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths recipes --ignore-src -r -y
colcon build
source install/setup.bash
```

Run a recipe's smoke test locally, exactly as CI does:

```bash
bash tools/smoke_test.sh rgc_lidar_bridge lidar_bridge.launch.py "/scan,/clock"
```

## Style & checks

- Install the hooks once: `pip install pre-commit && pre-commit install`, then
  `pre-commit run --all-files`.
- Markdown, links and spelling are checked in CI
  ([.github/workflows/lint.yml](.github/workflows/lint.yml)).

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/). Examples:

```text
feat(05-custom-world): add a world with obstacles and lighting
fix(03-lidar-bridge): correct the LaserScan frame_id
docs: clarify the headless rendering note in 00-setup
ci: assert /imu appears for the diff-drive recipe
```
