# 01 — Spawn a robot

**Verified by CI on:** Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic (gz-sim 8) · `ros_gz` (binary)

Spawn a robot model into an empty world from a single launch file. This is the
"hello world" of ROS 2 + Gazebo: start the simulator and place a model into it
with `ros_gz_sim`.

## Run it

```bash
# from the repo root, after `colcon build` and `source install/setup.bash`
ros2 launch rgc_spawn_robot spawn_robot.launch.py
```

A blue, box-bodied robot appears in an empty Gazebo world. The world starts
running on its own (`-r`), so you do not need to press ▶.

## What you should see

The Gazebo GUI with a ground plane and one model named `robot`.

<!-- When recorded, embed the demo here: docs/media/01-spawn-robot.gif -->
> No demo GIF yet — see [docs/media/RECORDING.md](../../docs/media/RECORDING.md) for the exact commands to record one.

## Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo → ROS |

## How it works

- `worlds/empty.sdf` declares the three core systems (`Physics`,
  `SceneBroadcaster`, `UserCommands`). `UserCommands` is what makes spawning
  possible. Declaring **any** `<plugin>` disables Gazebo's default auto-loaded
  systems, so all three are listed explicitly.
- The launch file includes `ros_gz_sim`'s `gz_sim.launch.py` to start Gazebo,
  then runs `ros_gz_sim create -file <model.sdf> -name robot` to spawn the model.
- A `parameter_bridge` brings `/clock` across so ROS nodes can run on sim time.

## Headless / CI

```bash
ros2 launch rgc_spawn_robot spawn_robot.launch.py headless:=true
```

Runs Gazebo server-only (`-s -r`) with no GUI — this is exactly what CI does
before asserting `/clock` is present.

## Troubleshooting

- **`Failed to load plugin`** — you likely copied an old `ignition-*` name.
  Harmonic uses `gz-sim-*-system` / `gz::sim::systems::*`.
- **Nothing spawns** — the world must include the `UserCommands` system.
- **`create` says the world is not ready** — make sure Gazebo actually launched
  (check for errors above) and that `gz_args` points at a valid world file.
