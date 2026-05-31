# 08 — Spawn from Gazebo Fuel

**Verified by CI on:** Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic (gz-sim 8) · `ros_gz` (binary)

Pull ready-made models from [Gazebo Fuel](https://app.gazebosim.org/) into your
world by URI — no need to model everything yourself.

## Run it

```bash
# from the repo root, after `colcon build` and `source install/setup.bash`
# (the first run downloads the models, so you need internet access)
ros2 launch rgc_spawn_from_fuel spawn_from_fuel.launch.py
```

## What you should see

A construction cone and a construction barrel sitting on the ground — both pulled
straight from Fuel.

<!-- When recorded, embed the demo here: docs/media/08-spawn-from-fuel.gif -->
> No demo GIF yet — see [docs/media/RECORDING.md](../../docs/media/RECORDING.md) for the exact commands to record one.

## Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo → ROS |

## How it works

- `worlds/fuel_world.sdf` uses `<include><uri>` with full Fuel URLs, e.g.
  `https://fuel.gazebosim.org/1.0/OpenRobotics/models/Construction Cone`. Gazebo
  downloads and caches the model on first load (`~/.gz/fuel`).
- Swap the URIs for any model on Fuel — browse them at
  <https://app.gazebosim.org/>.
- You can also spawn a Fuel model dynamically with
  `ros2 run ros_gz_sim create -name thing -file "<fuel-uri>"`.

## Headless / CI

```bash
ros2 launch rgc_spawn_from_fuel spawn_from_fuel.launch.py headless:=true
```

CI asserts `/clock` appears. The Fuel download is a bonus: if Fuel is briefly
unreachable, Gazebo logs a warning and the world still loads, so the check stays
honest about what it proves.

## Troubleshooting

- **Models do not appear** — check your internet connection and look for Fuel
  download warnings in the Gazebo output; the cache lives in `~/.gz/fuel`.
- **Slow first start** — that is the one-time download; later runs use the cache.
