# Day 5 Solutions

## 1. Liveness probe (exec)
```yaml
containers:
- name: liveness
  image: busybox
  command: ["sh", "-c", "touch /tmp/healthy; sleep 30; rm -f /tmp/healthy; sleep 600"]
  livenessProbe:
    exec:
      command: ["cat", "/tmp/healthy"]
    periodSeconds: 5
```
Watch restarts: `kubectl get pod liveness-exec -w`

## 2. Readiness probe (httpGet)
```yaml
readinessProbe:
  httpGet: {path: /, port: 80}
  initialDelaySeconds: 5
```
`kubectl get pod readiness-http -w` — READY flips from 0/1 to 1/1 after the delay.

## 3. Startup probe for a slow app
```yaml
startupProbe:
  exec: {command: ["cat", "/tmp/started"]}
  failureThreshold: 30
  periodSeconds: 1
livenessProbe:
  exec: {command: ["cat", "/tmp/started"]}
  periodSeconds: 3
```
While `startupProbe` hasn't succeeded, `livenessProbe` is not evaluated — this is the exam-relevant behavior to confirm.

## 4. Broken probe debugging
```
kubectl describe pod <pod>     # check Events for "Liveness probe failed"
kubectl logs <pod> --previous
kubectl edit pod <pod>         # or patch deployment with correct path/port
```

## 5. kubectl debug on a crashlooping Pod
```
kubectl debug <pod> -it --image=busybox --share-processes --copy-to=<pod>-debug -- sh
```
Inspect filesystem/processes from the copy without disturbing the original.

## 6. postStart / preStop hooks
```yaml
lifecycle:
  postStart:
    exec: {command: ["sh", "-c", "echo started > /tmp/poststart"]}
  preStop:
    exec: {command: ["sh", "-c", "sleep 5"]}
spec:
  terminationGracePeriodSeconds: 30
```
`kubectl delete pod <pod>` and time how long it takes to actually terminate (should be ~5s+ due to preStop).

## 7. Logs across restarts
```
kubectl logs <pod>
kubectl logs <pod> --previous
```

## 8. Multi-container logs
```
kubectl logs <pod> -c <container-name>
kubectl logs <pod> --all-containers=true
```
