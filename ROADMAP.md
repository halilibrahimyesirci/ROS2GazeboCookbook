# Roadmap — ROS 2 + Gazebo Cookbook

> Minimal, copy-paste-able, **actually-working** examples for modern ROS 2 and the new Gazebo.
> Each recipe is self-contained, runs with a single command, and targets one common task people get stuck on.

**Why this exists:** Gazebo Classic reached end-of-life (Jan 2025) and ROS 1 followed (May 2025), forcing the whole community onto ROS 2 + the new Gazebo (`gz-sim` / `ros_gz`). Working open-source examples for this stack are still scarce and scattered, and most search results point to outdated ROS 1 + Gazebo Classic material. This repo aims to be the go-to, up-to-date reference cookbook.

---

## Primary target stack

| Component | Primary (tested) | Also targeting |
|-----------|------------------|----------------|
| ROS 2     | Jazzy Jalisco (LTS) | Latest distro |
| Gazebo    | Harmonic (LTS, supported to ~2028) | Jetty (latest) |
| OS        | Ubuntu 24.04 | Ubuntu 22.04 |
| Bridge    | `ros_gz` (`ros_gz_bridge`, `ros_gz_sim`, `ros_gz_image`) | — |

Every recipe states the exact versions it was verified on. When a recipe breaks on a new distro, that is tracked as an issue, not silently left to rot.

---

## Status legend

- ✅ Done — complete and CI-verified (recipes also have a demo GIF)
- 🟢 Shipped — recipe runs and is CI-verified; demo GIF still pending
- 🚧 In progress
- 📋 Planned
- 💡 Idea / needs scoping

---

## v0.1 — MVP (the first useful release)

Goal: a person Googling a basic task finds this repo, clones it, and it works in 5 minutes.

- ✅ `00-setup` — install ROS 2 Jazzy + Gazebo Harmonic, verify the bridge, troubleshooting notes
- 🟢 `01-spawn-robot` — spawn a robot into an empty world (SDF + launch)
- 🟢 `02-camera-bridge` — camera sensor → `ros_gz_bridge` → ROS topic, viewed in `rqt`/RViz
- 🟢 `03-lidar-bridge` — 2D LiDAR bridged to ROS, visualized in RViz
- 🟢 `04-diffdrive-teleop` — differential drive robot + IMU + keyboard teleop
- ✅ Top-level README with a recipe index (one row per keyword) and a 1-command quick start

**Release criteria:** all four recipes run from a clean Ubuntu install, each has its own short README and a GIF. Code + CI are in place; the remaining gate for v0.1 is recording a demo GIF per recipe (see `docs/media/RECORDING.md`).

---

## v0.2 — Worlds & visualization

- 📋 `05-custom-world` — build a world with obstacles, lighting and materials
- 📋 `06-rviz-config` — ready-made RViz configs for camera + LiDAR + TF
- 📋 `07-multiple-sensors` — one robot carrying camera + LiDAR + IMU, all bridged cleanly
- 💡 `08-spawn-from-fuel` — pull and spawn models from Gazebo Fuel

---

## v0.3 — Navigation & autonomy

- 📋 `09-nav2-basic` — Nav2 stack driving the diff-drive robot to a goal in simulation
- 📋 `10-slam` — build a map with SLAM, then navigate it
- 💡 `11-behavior` — a small autonomous patrol/explore behavior on top of Nav2

---

## v0.4 — Migration kit (high-search, high-value)

A focused section for people forced to move off Gazebo Classic.

- 📋 `migration/cheatsheet.md` — `gazebo_ros_pkgs` → `ros_gz` mapping, plugin equivalents, SDF changes
- 📋 `migration/before-after` — the same robot shown in Classic and in new Gazebo, side by side
- 💡 `migration/common-errors.md` — the bridge/plugin/SDF errors people actually hit, with fixes

---

## v1.0 — A reference robot

- 💡 `reference-robot` — one clean, well-modeled mobile robot (diff-drive + camera + LiDAR + IMU) that ties the recipes together: teleop, SLAM, Nav2, RViz, all working out of the box
- 💡 Docker image + devcontainer so anyone can run everything with zero local setup
- 💡 CI that launches each recipe headless and fails the build if a recipe stops working

---

## Beyond v1.0 (ideas)

- 💡 C++ versions of the recipes (Gazebo's C++ side is notably under-documented)
- 💡 Multi-robot example with namespacing
- 💡 Manipulation: a simple arm + MoveIt 2 in new Gazebo
- 💡 Perception recipe: bridge a camera into a vision pipeline (e.g. detection)
- 💡 Sim-to-real notes: what changes when you move a recipe onto real hardware

---

## Scope & non-goals

**In scope:** minimal, single-purpose, current, runnable examples that fill the documentation gap for ROS 2 + new Gazebo.

**Not in scope:** being a full robotics framework, replacing the official docs, supporting end-of-life stacks (ROS 1 / Gazebo Classic) beyond the migration section, or large monolithic projects. Small and working beats big and broken.

---

## How to contribute

Recipes, fixes, and "this broke on distro X" reports are all welcome. The bar for a recipe is simple: it must run from a clean install with one command, have a short README, and state the versions it was tested on. Open an issue before a large addition so we can keep recipes minimal and consistent.

---

*Last updated: May 2026 · Roadmap is intentionally living — dates are deliberately omitted; milestones ship when they meet their release criteria.*
