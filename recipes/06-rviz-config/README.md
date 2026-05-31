# 06 — RViz configs

**Verified by CI on:** Ubuntu 24.04 · ROS 2 Jazzy (builds in CI; RViz itself is a GUI, so it is run by hand)

Reusable RViz configurations so you do not have to rebuild displays every time.
This package is meant to be run **alongside** a sim recipe.

## Configs

| Config | Shows |
|--------|-------|
| `combined` | camera image + LiDAR scan + TF + grid (fixed frame `base_link`) |
| `tf_only` | just the TF tree and a grid (handy for debugging frames) |

## Run it

Start a sim recipe with its own RViz turned off, then open a config here:

```bash
# terminal 1 — a multi-sensor sim, without its built-in RViz
ros2 launch rgc_multiple_sensors multiple_sensors.launch.py rviz:=false

# terminal 2 — open a ready-made view
ros2 launch rgc_rviz_config rviz.launch.py config:=combined
```

<!-- When recorded, embed the demo here: docs/media/06-rviz-config.gif -->
> No demo GIF yet — see [docs/media/RECORDING.md](../../docs/media/RECORDING.md) for the exact commands to record one.

## How it works

- `rviz/*.rviz` are plain RViz config files you can also load directly with
  `rviz2 -d <file>.rviz`.
- `launch/rviz.launch.py` just opens RViz with the chosen config and
  `use_sim_time` set, so timestamps line up with the simulator.

## Notes

- RViz is a GUI, so there is nothing to smoke-test headless — CI verifies that
  this package **builds and installs** its configs. The views themselves are run
  by hand.
- Fixed frame is `base_link`; the sim recipes publish the matching TF frames.

## Troubleshooting

- **Displays are empty** — make sure a sim recipe is publishing `/camera`,
  `/scan` and the TF frames, and that the fixed frame is `base_link`.
- **Wrong config opens** — pass `config:=tf_only` (the file name without `.rviz`).
