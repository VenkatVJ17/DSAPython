# Day 5 — Observability & Maintenance

## 1. Liveness probe (exec) (4 min)
Create a Pod `liveness-exec` (image `busybox`) that creates `/tmp/healthy` on start then deletes it after 30s (`sh -c "touch /tmp/healthy; sleep 30; rm -f /tmp/healthy; sleep 600"`). Add a liveness probe using `cat /tmp/healthy`, `periodSeconds=5`. Watch it get restarted after the file disappears.

## 2. Readiness probe (httpGet) (5 min)
Create a Pod `readiness-http` (image `nginx`) with a readiness probe on `httpGet path=/ port=80`, `initialDelaySeconds=5`. Confirm it shows `READY 1/1` only after the delay, and check `kubectl describe pod` events.

## 3. Startup probe for a slow app (5 min)
Add a `startupProbe` (exec, generous `failureThreshold`/`periodSeconds`) to a Pod simulating a 20s boot time, alongside a liveness probe with a short period — confirm liveness checks don't kill the Pod before startup probe succeeds.

## 4. Broken probe debugging (8 min)
Deploy a Pod with a deliberately wrong liveness probe (wrong port or wrong path). Observe it crash-looping. Diagnose via `kubectl describe pod` events and `kubectl logs --previous`. Fix it with `kubectl edit` or patch.

## 5. kubectl debug on a crashlooping Pod (7 min)
Create a Pod that crashes immediately (`busybox` with a bad command). Use `kubectl debug` to create a debug container/copy with an overridden command to inspect the filesystem, rather than just reading logs.

## 6. postStart / preStop hooks (5 min)
Add a `postStart` exec hook that writes a file, and a `preStop` exec hook that sleeps 5s before termination (graceful shutdown simulation). Delete the Pod and observe the delay caused by `preStop` + confirm `terminationGracePeriodSeconds`.

## 7. Logs across restarts (3 min)
Force a container to restart (crash it). Compare `kubectl logs <pod>` (current) vs `kubectl logs <pod> --previous` (prior instance).

## 8. Multi-container logs (3 min)
On a Pod with 2+ containers, fetch logs scoped to one specific container with `-c`, and combined with `--all-containers=true`.
