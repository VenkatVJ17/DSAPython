# Day 2 Solutions

## 1. Init container gate
```
kubectl run web-init --image=nginx --dry-run=client -o yaml > web-init.yaml
```
Edit to add:
```yaml
spec:
  initContainers:
  - name: wait-for-file
    image: busybox
    command: ["sh", "-c", "sleep 5"]
  containers:
  - name: nginx
    image: nginx
```

## 2. Sidecar log shipper
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-sidecar
spec:
  volumes:
  - name: logs
    emptyDir: {}
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "while true; do echo $(date) >> /var/log/app.log; sleep 2; done"]
    volumeMounts:
    - name: logs
      mountPath: /var/log
  - name: log-agent
    image: busybox
    command: ["sh", "-c", "tail -f /var/log/app.log"]
    volumeMounts:
    - name: logs
      mountPath: /var/log
```

## 3. Ambassador pattern
Same shape as #2 but no shared volume needed — both containers share the Pod's network namespace automatically, so `main` reaching `localhost:8080` will hit `ambassador`'s nginx on port 80... note: nginx default listens on 80, not 8080. Either set nginx to listen on 8080 via a ConfigMap-mounted config, or have `main` curl `localhost:80`. The teaching point: containers in one Pod share `localhost`.

## 4. Labels & selectors
```
kubectl run pod-a --image=busybox --labels=env=prod,tier=web -- sleep 3600
kubectl run pod-b --image=busybox --labels=env=prod,tier=db -- sleep 3600
kubectl run pod-c --image=busybox --labels=env=dev,tier=web -- sleep 3600
kubectl get pods -l env=prod
kubectl get pods -l tier=web
kubectl get pods -l env=prod,tier=web
kubectl label pod pod-a checked=true
kubectl label pod pod-c tier-
```

## 5. Adapter pattern
Same shared-`emptyDir` shape as #2, with `adapter` running a `sed`/`awk` transform on the tail of the shared file.

## 6. Resource requests/limits
```yaml
resources:
  requests: {cpu: "50m", memory: "64Mi"}
  limits: {cpu: "100m", memory: "128Mi"}
```
Half for `log-agent`: requests cpu=25m/memory=32Mi, limits cpu=50m/memory=64Mi.
