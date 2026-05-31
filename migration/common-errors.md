# Common migration errors

The errors people actually hit moving from Gazebo Classic to the new Gazebo, and
how to fix each.

## `Failed to load plugin libgazebo_ros_*.so`

You are running the new Gazebo with a Classic model. `libgazebo_ros_*` plugins do
not exist there. Replace them with the equivalent **gz-sim system** and bridge
the topic — see the [cheatsheet](cheatsheet.md#the-big-difference-plugins--systems--bridge).

## `Failed to load plugin ... ignition-...` / unknown `ignition.msgs`

You copied a Fortress-era (or older) tutorial. Garden and later renamed
everything `ignition*` → `gz*`:

- `ignition-gazebo-*-system` → `gz-sim-*-system`
- `ignition::gazebo::systems::*` → `gz::sim::systems::*`
- `ignition.msgs.*` → `gz.msgs.*`
- `ign sim` / `ign gazebo` → `gz sim`

## My robot spawns but nothing simulates / I can't spawn into the world

Declaring any `<plugin>` in a world turns off Gazebo's auto-loaded defaults. Add
the core systems explicitly:

```xml
<plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
<plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
<plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
```

`UserCommands` is the one that lets you spawn models.

## The bridge prints nothing / no data on the ROS topic

1. **Wrong gz type string** — it must be exactly `gz.msgs.Image`, `gz.msgs.IMU`
   (capitals), `gz.msgs.LaserScan`, etc. See the
   [type map](cheatsheet.md#message-type-bridge-map).
2. **The world is paused** — start it running with `-r` in `gz_args`.
3. **No system to produce the data** — a camera/LiDAR needs
   `gz-sim-sensors-system`; an IMU needs its own `gz-sim-imu-system`.

## Camera/LiDAR topic exists but the image/scan is empty

The sensor is declared but not rendered. Make sure the world has the
`gz-sim-sensors-system` with a render engine:

```xml
<plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
  <render_engine>ogre2</render_engine>
</plugin>
```

Headless (no display)? Render off-screen with EGL:
`gz sim -s -r --headless-rendering world.sdf` (and leave `DISPLAY` unset).

## RViz shows nothing / "Fixed Frame does not exist"

- Set `use_sim_time:=true` on your ROS nodes **and** bridge `/clock`, or
  timestamps will not line up.
- The bridged message's `frame_id` may be a scoped gz name RViz cannot resolve.
  Override it in the bridge YAML with the `frame_id:` key, and publish a matching
  `static_transform_publisher`. See [recipe 03](../recipes/03-lidar-bridge/).

## The diff-drive robot does not move

- `cmd_vel` must be bridged **ROS → GZ** (`direction: ROS_TO_GZ`), and the
  plugin's `<topic>` must match the gz topic you bridge to.
- Confirm the plugin is `gz-sim-diff-drive-system` with valid `<left_joint>` /
  `<right_joint>` / `<wheel_separation>` / `<wheel_radius>`.

## `Twist` vs `TwistStamped`

ROS 2 is moving controllers toward `geometry_msgs/msg/TwistStamped`. Both bridge
to `gz.msgs.Twist`. Pick the one your publisher uses (`teleop_twist_keyboard`
defaults to `Twist`; pass `-p stamped:=true` for `TwistStamped`).
