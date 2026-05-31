# Recording demo GIFs

Every recipe is verified in CI (build + headless launch + topics), but a short
demo GIF is what makes it click. GIFs can't be produced in CI (it has no display
and no GPU), so they're recorded by hand on a Linux machine. This guide gives the
exact steps.

**Target:** a ~5–10 s, ~960 px-wide GIF per recipe, committed as
`docs/media/<NN>-<recipe>.gif` and referenced from that recipe's README.

## Tools

Pick a recorder for your session type:

```bash
# X11: Peek exports GIF directly
sudo apt install peek

# Wayland: record MP4 with wf-recorder, then convert with ffmpeg
sudo apt install wf-recorder ffmpeg slurp
```

## Record

1. Launch the recipe **with the GUI** (do _not_ pass `headless:=true`):

   ```bash
   ros2 launch rgc_lidar_bridge lidar_bridge.launch.py
   ```

2. Arrange the windows you want in frame (Gazebo and/or RViz).

3. Capture:

   - **Peek (X11):** open Peek, drag it over the area, click *Record as GIF*.
   - **Wayland:**

     ```bash
     wf-recorder -g "$(slurp)" -f /tmp/demo.mp4     # select a region; Ctrl-C to stop
     ffmpeg -i /tmp/demo.mp4 -vf "fps=12,scale=960:-1:flags=lanczos" \
       docs/media/03-lidar-bridge.gif
     ```

4. Keep it small (aim for < 5 MB). If it's too big, drop the fps to 10, the width
   to 800, or trim the clip.

## Wire it into the README

Replace the placeholder comment in the recipe's README with the image:

```markdown
![demo](../../docs/media/03-lidar-bridge.gif)
```

Then the recipe can move from `🟢 code + CI` to `✅ done` in the root README
once the GIF is committed.

## Suggested shots

| Recipe | Show |
|--------|------|
| 01-spawn-robot | the robot appearing in the empty Gazebo world |
| 02-camera-bridge | the RViz Image panel showing the red box |
| 03-lidar-bridge | the 360° scan ring picking out the three boxes in RViz |
| 04-diffdrive-teleop | driving around the pillars; the odometry trail in RViz |
