#!/usr/bin/env bash
#
# Launch a recipe headless and wait until the expected ROS topics appear.
# This is the gating "Tier 2" check used by CI: it proves a recipe builds,
# launches without crashing, and wires up the topics it claims to.
#
# Usage:
#   tools/smoke_test.sh <package> <launch_file> <comma_separated_topics> [timeout_s]
#
# Example:
#   tools/smoke_test.sh rgc_lidar_bridge lidar_bridge.launch.py "/scan,/clock"
#
set -uo pipefail

PKG="${1:?package name required}"
LAUNCH="${2:?launch file required}"
TOPICS="${3:?comma-separated topics required}"
TIMEOUT="${4:-45}"

LOG="$(mktemp)"
echo "[smoke] launching: ros2 launch ${PKG} ${LAUNCH} headless:=true rviz:=false"
ros2 launch "${PKG}" "${LAUNCH}" headless:=true rviz:=false >"${LOG}" 2>&1 &
LAUNCH_PID=$!

cleanup() {
  kill -INT "${LAUNCH_PID}" 2>/dev/null || true
  for _ in 1 2 3 4 5; do
    kill -0 "${LAUNCH_PID}" 2>/dev/null || break
    sleep 1
  done
  kill -KILL "${LAUNCH_PID}" 2>/dev/null || true
}
trap cleanup EXIT

IFS=',' read -ra WANT <<<"${TOPICS}"

end=$((SECONDS + TIMEOUT))
while [ "${SECONDS}" -lt "${end}" ]; do
  if ! kill -0 "${LAUNCH_PID}" 2>/dev/null; then
    echo "[smoke] FAIL: launch process exited early"
    echo "----- launch log -----"
    cat "${LOG}"
    exit 1
  fi

  have="$(ros2 topic list 2>/dev/null || true)"
  missing=0
  for t in "${WANT[@]}"; do
    printf '%s\n' "${have}" | grep -qx "${t}" || missing=1
  done

  if [ "${missing}" -eq 0 ]; then
    echo "[smoke] OK: all expected topics present: ${WANT[*]}"
    exit 0
  fi
  sleep 2
done

echo "[smoke] FAIL: not all expected topics appeared within ${TIMEOUT}s"
echo "[smoke] wanted: ${WANT[*]}"
echo "[smoke] currently visible:"
ros2 topic list 2>/dev/null || true
echo "----- launch log -----"
cat "${LOG}"
exit 1
