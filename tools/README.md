# tools

Helper scripts used by CI (and handy locally).

- **`smoke_test.sh`** — launch a recipe headless and assert the expected ROS
  topics appear. This is the gating check: build + launch + topics present.
- **`data_check.sh`** — best-effort check that a real message arrives on a data
  topic. Non-gating, because software rendering in CI is not perfectly reliable.

Run one locally after building and sourcing the workspace:

```bash
bash tools/smoke_test.sh rgc_lidar_bridge lidar_bridge.launch.py "/scan,/clock"
```
