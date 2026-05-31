# 05 — Custom world

**Verified by CI on:** Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic (gz-sim 8) · `ros_gz` (binary)

Build a world worth driving around in: a walled arena with a tinted ground, two
lights (a directional sun and a warm point light), and a handful of colored
obstacles — then spawn a robot into it.

## Run it

```bash
# from the repo root, after `colcon build` and `source install/setup.bash`
ros2 launch rgc_custom_world custom_world.launch.py
```

## What you should see

A 5 m square arena with walls, a red box, a green cylinder and a blue box, lit by
a sun plus a warm overhead lamp, with the robot in the middle.

<!-- When recorded, embed the demo here: docs/media/05-custom-world.gif -->
> No demo GIF yet — see [docs/media/RECORDING.md](../../docs/media/RECORDING.md) for the exact commands to record one.

## Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo → ROS |

## How it works

- `worlds/custom_world.sdf` shows the world-building pieces: a `<scene>` (ambient
  light, sky background, shadows), two `<light>` elements (a `directional` sun
  and a `point` lamp with `<attenuation>`), `<material>` colors on every visual,
  four wall models and a few obstacle models.
- The launch file starts Gazebo on this world and spawns the robot with
  `ros_gz_sim create`, then bridges `/clock`.

## Headless / CI

```bash
ros2 launch rgc_custom_world custom_world.launch.py headless:=true
```

No rendered sensors here, so plain `-s -r` is enough. CI asserts `/clock` appears.

## Troubleshooting

- **World looks flat/black** — check the `<scene>` and `<light>` blocks; with no
  light, materials render dark.
- **Robot falls through or spawns oddly** — adjust the spawn pose (`-z`) so the
  wheels start just above the ground.
