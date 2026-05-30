#!/usr/bin/env bash
#
# Best-effort "Tier 3" check: launch a recipe headless and confirm at least one
# real message arrives on a data topic. GPU-less software rendering in CI is not
# 100% reliable, so this is intentionally NON-gating (CI runs it with
# continue-on-error) - it is informative, not a pass/fail wall.
#
# Usage:
#   tools/data_check.sh <package> <launch_file> <topic> [timeout_s]
#
# Example:
#   tools/data_check.sh rgc_lidar_bridge lidar_bridge.launch.py "/scan"
#
set -uo pipefail

PKG="${1:?package name required}"
LAUNCH="${2:?launch file required}"
TOPIC="${3:?topic required}"
TIMEOUT="${4:-40}"

LOG="$(mktemp)"
echo "[data] launching: ros2 launch ${PKG} ${LAUNCH} headless:=true rviz:=false"
ros2 launch "${PKG}" "${LAUNCH}" headless:=true rviz:=false >"${LOG}" 2>&1 &
LAUNCH_PID=$!
trap 'kill -INT "${LAUNCH_PID}" 2>/dev/null || true; sleep 2; kill -KILL "${LAUNCH_PID}" 2>/dev/null || true' EXIT

# Give the simulator time to start producing data before we listen.
sleep 12

echo "[data] waiting up to ${TIMEOUT}s for one message on ${TOPIC} ..."
if timeout "${TIMEOUT}" ros2 topic echo --once "${TOPIC}" >/dev/null 2>&1; then
  echo "[data] OK: received a message on ${TOPIC}"
  exit 0
fi

echo "[data] no message on ${TOPIC} within ${TIMEOUT}s (best-effort tier; not a build failure)"
echo "----- launch log (tail) -----"
tail -n 40 "${LOG}" || true
exit 1
