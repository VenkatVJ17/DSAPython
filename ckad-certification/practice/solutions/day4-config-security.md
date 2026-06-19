# Day 4 Solutions

## 1. ConfigMap from literals + file
```
kubectl create configmap app-config --from-literal=LOG_LEVEL=debug --from-literal=MAX_CONNECTIONS=100
printf 'key1=value1\nkey2=value2\n' > config.env
kubectl create configmap app-config-file --from-file=config.env
```

## 2. Consume ConfigMap as env vars
```yaml
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "env; sleep 3600"]
    envFrom:
    - configMapRef:
        name: app-config
```
```
kubectl exec cm-env-pod -- env | grep -E 'LOG_LEVEL|MAX_CONNECTIONS'
```

## 3. Consume ConfigMap as a volume
```yaml
spec:
  volumes:
  - name: config-vol
    configMap:
      name: app-config
  containers:
  - name: app
    volumeMounts:
    - name: config-vol
      mountPath: /etc/config
```
```
kubectl exec cm-vol-pod -- ls /etc/config
kubectl exec cm-vol-pod -- cat /etc/config/LOG_LEVEL
```

## 4. Secret + single-key env injection
```
kubectl create secret generic db-secret --from-literal=username=admin --from-literal=password=s3cr3t
```
```yaml
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: password
```
```
kubectl exec <pod> -- env | grep DB_PASSWORD
```

## 5. SecurityContext at Pod and container level
```yaml
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: secure
    image: busybox
    command: ["sleep", "3600"]
    securityContext:
      runAsUser: 2000
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
```
```
kubectl exec secure-pod -- id   # uid=2000 confirms container-level override wins
```

## 6. ResourceQuota + LimitRange
```
kubectl create namespace quota-test
```
```yaml
# resourcequota.yaml
apiVersion: v1
kind: ResourceQuota
metadata: {name: quota, namespace: quota-test}
spec:
  hard: {pods: "3", requests.cpu: "1"}
---
# limitrange.yaml
apiVersion: v1
kind: LimitRange
metadata: {name: limits, namespace: quota-test}
spec:
  limits:
  - default: {cpu: "200m"}
    defaultRequest: {cpu: "100m"}
    type: Container
```
```
kubectl apply -f resourcequota.yaml -f limitrange.yaml
kubectl run t1 -n quota-test --image=busybox -- sleep 3600
kubectl describe pod t1 -n quota-test   # confirm default cpu request/limit applied
```

## 7. ServiceAccount + mount
```
kubectl create serviceaccount app-sa
kubectl run sa-pod --image=busybox --overrides='{"spec":{"serviceAccountName":"app-sa"}}' -- sleep 3600
kubectl exec sa-pod -- ls /var/run/secrets/kubernetes.io/serviceaccount
```

## 8. Speed round
```
kubectl create secret generic mysecret --from-literal=k1=v1 --from-literal=k2=v2
kubectl create configmap mycm --from-file=./somedir/
kubectl create secret docker-registry myregsecret --docker-server=<server> --docker-username=<u> --docker-password=<p> --docker-email=<e>
kubectl run mypod --image=nginx --dry-run=client -o yaml
```
