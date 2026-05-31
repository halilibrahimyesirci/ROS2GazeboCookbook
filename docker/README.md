# Docker

Run the whole cookbook with zero local ROS/Gazebo install.

## Build

```bash
docker build -t ros2gazebo-cookbook .
```

## Run (headless)

```bash
docker run --rm -it ros2gazebo-cookbook
# inside the container:
ros2 launch rgc_reference_robot reference_robot.launch.py headless:=true
```

The image already has the workspace built and sourced (via the entrypoint), so
recipes are ready to launch.

## Run with the Gazebo / RViz GUI (Linux + X11)

```bash
xhost +local:root   # allow the container to use your X server (revoke later with: xhost -local:root)
docker run --rm -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --net=host \
  ros2gazebo-cookbook \
  ros2 launch rgc_reference_robot reference_robot.launch.py
```

## VS Code Dev Container

Open the repo in VS Code with the **Dev Containers** extension and "Reopen in
Container" — it uses [`.devcontainer/devcontainer.json`](../.devcontainer/devcontainer.json),
which builds this same image.
