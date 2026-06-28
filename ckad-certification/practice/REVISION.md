---
tags: [ckad, kubernetes, revision, exam-prep]
created: 2026-06-28
---

# CKAD Revision — killer.sh Cheatsheet

## Revision Checklist
- [ ] Domain 1 — Pod Design Patterns
- [ ] Domain 2 — Application Deployment
- [ ] Domain 3 — Configuration & Security ⚠️ 25% of exam
- [ ] Domain 4 — Observability
- [ ] Domain 5 — Services & Networking

---

## Exam Setup — Run First Every Session

```bash
alias k=kubectl
alias kd='kubectl describe'
alias kg='kubectl get'
alias kaf='kubectl apply -f'
export do='--dry-run=client -o yaml'
export now='--force --grace-period=0'
```

> [!TIP] vi YAML settings — run before editing any file
> `:set shiftwidth=2 tabstop=2 expandtab`
> `:%retab!` — fixes tabs after a bad paste
> `:set paste` — run in **normal mode** BEFORE pressing `o` to paste from docs

> [!TIP] Generate file without vi paste issues
> `cat > pod.yaml << 'EOF'` ... `EOF` — type entire YAML in terminal, no paste mangling

---

## Domain 1 — Pod Design Patterns

### Multi-container YAML Skeleton

```yaml
spec:
  volumes:
  - name: shared
    emptyDir: {}
  initContainers:
  - name: init
    image: busybox
    command: ["sh", "-c", "sleep 5"]       # must exit 0 before main starts
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "while true; do echo log >> /data/app.log; sleep 2; done"]
    volumeMounts:
    - name: shared
      mountPath: /data
  - name: sidecar
    image: busybox
    command: ["sh", "-c", "tail -f /data/app.log"]
    volumeMounts:
    - name: shared
      mountPath: /data
```

### Pattern Table

| Pattern | Mechanic | Remember |
|---|---|---|
| **Init container** | Runs before app, must exit 0 | No `kubectl run` flag — `--dry-run` + edit |
| **Sidecar** | Shared `emptyDir` volume | Both containers mount same volume name |
| **Ambassador** | Shared network namespace | `localhost:<port>` to reach sibling container |
| **Adapter** | Shared `emptyDir` + transforms output | Use `awk + fflush()` NOT `sed` |

> [!WARNING] Adapter pattern — sed buffering trap
> `tail -f | sed` shows no output for minutes because sed blocks when stdout is a pipe.
> Use `awk '{print $0; fflush()}'` instead — forces flush every line.

### Labels

```bash
kubectl run pod-a --image=busybox --labels=env=prod,tier=web -- sleep 3600
kubectl get pods -l env=prod,tier=web     # comma = AND (no OR in basic selector)
kubectl label pod pod-a checked=true      # add label
kubectl label pod pod-c tier-             # remove label (trailing dash)
```

### Resources

```yaml
resources:
  requests: {cpu: "50m", memory: "64Mi"}   # scheduler uses this to place pod
  limits:   {cpu: "100m", memory: "128Mi"} # enforced at runtime
```

> [!NOTE]
> Exceed **memory limit** → OOMKill (container dies)
> Exceed **CPU limit** → throttled (container slows, not killed)

---

## Domain 2 — Application Deployment

### Core Commands

```bash
kubectl create deployment web --image=nginx:1.25 --replicas=3
kubectl scale deployment web --replicas=5
kubectl set image deployment/web nginx=nginx:1.26   # nginx = container name
kubectl rollout status deployment/web               # blocks until complete
kubectl rollout history deployment/web
kubectl rollout undo deployment/web                 # back 1 revision
kubectl rollout undo deployment/web --to-revision=2
```

> [!WARNING] `set image` — container name not image name
> `nginx=nginx:1.26` — left side is the **container name** from the spec, not the image.
> Check with `kubectl describe deployment web` if unsure.

### Zero-Downtime Rollout

```bash
kubectl patch deployment web -p \
  '{"spec":{"strategy":{"rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'
```

| Setting | Meaning |
|---|---|
| `maxUnavailable=0` | Never drop below desired count |
| `maxSurge=1` | Allow 1 extra pod temporarily |

### Canary Pattern

```bash
kubectl create deployment web-stable --image=nginx:1.25 --replicas=3
kubectl create deployment web-canary  --image=nginx:1.26 --replicas=1
kubectl expose deployment web-stable --name=web-svc --port=80 --selector=app=web
```

> [!WARNING] Canary — always set `--selector` explicitly
> Without `--selector=app=web`, expose copies deployment's own selector (`app=web-stable`) and misses canary pods entirely.

Traffic split = replica ratio → 3 stable : 1 canary = 75/25 split.

### Helm

```bash
helm create mychart
helm install demo ./mychart
helm upgrade demo ./mychart --set replicaCount=5
helm history demo
helm rollback demo 1
```

### Kustomize

```bash
kubectl apply -k overlay/dev
```

```yaml
# overlay/dev/kustomization.yaml
resources: [../../base]
replicas:
- name: web
  count: 3
labels:
- pairs: {env: dev}
  includeSelectors: false
```

---

## Domain 3 — Configuration & Security ⚠️ 25% of Exam

### ConfigMap

```bash
# Literals
kubectl create configmap app-config --from-literal=LOG_LEVEL=debug --from-literal=MAX=100

# From file
kubectl create configmap cm --from-file=config.env      # whole file = 1 key
kubectl create configmap cm --from-env-file=config.env  # each line = 1 key
```

> [!DANGER] `--from-file` vs `--from-env-file`
> `--from-file` → 1 key named after the filename, value is entire file contents
> `--from-env-file` → each `key=value` line becomes a separate key
> Wrong choice = silent mismatch at runtime

**3 ways to inject ConfigMap into a Pod:**

```yaml
# 1. All keys as env vars
envFrom:
- configMapRef:
    name: app-config

# 2. Single key as env var (with rename)
env:
- name: LOG_LEVEL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: LOG_LEVEL

# 3. Volume mount (each key = file)
volumes:
- name: config-vol
  configMap:
    name: app-config
volumeMounts:
- name: config-vol
  mountPath: /etc/config
```

> [!NOTE] env vs volume — live update difference
> **env vars** → captured at pod start, NOT updated when ConfigMap changes
> **volume mount** → live-updated within ~1 min without pod restart

### Secret

```bash
kubectl create secret generic db-secret \
  --from-literal=username=admin --from-literal=password=s3cr3t

kubectl create secret docker-registry myregsecret \
  --docker-server=<server> --docker-username=<u> \
  --docker-password=<p> --docker-email=<e>
```

```yaml
# Single key injection
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: password
```

> [!NOTE]
> Secrets are stored base64-encoded in etcd (not encrypted by default).
> Kubernetes decodes before injection — app always sees plaintext.

### SecurityContext

```yaml
spec:
  securityContext:              # Pod level
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000               # Pod-only — no container-level equivalent
  containers:
  - name: app
    securityContext:            # Container level — wins over pod level
      runAsUser: 2000
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
```

> [!NOTE] Pod vs Container securityContext
> Container-level **wins** for same field.
> `fsGroup` is **Pod-only** — sets group ownership on mounted volumes.

### ResourceQuota + LimitRange

```yaml
apiVersion: v1
kind: ResourceQuota
metadata: {name: quota, namespace: quota-test}
spec:
  hard: {pods: "3", requests.cpu: "1"}
---
apiVersion: v1
kind: LimitRange
metadata: {name: limits, namespace: quota-test}
spec:
  limits:
  - default: {cpu: "200m"}         # limit (ceiling)
    defaultRequest: {cpu: "100m"}  # request (floor)
    type: Container
```

> [!WARNING] Always pair these together
> Once `requests.cpu` quota exists, every pod MUST have a CPU request or it gets rejected.
> LimitRange fills that gap by injecting defaults — without it, unspecified pods break.

### ServiceAccount

```bash
kubectl create serviceaccount app-sa
kubectl run sa-pod --image=busybox \
  --overrides='{"spec":{"serviceAccountName":"app-sa"}}' -- sleep 3600
kubectl exec sa-pod -- ls /var/run/secrets/kubernetes.io/serviceaccount
```

> [!TIP]
> `--overrides` = inject any field kubectl run has no flag for (pass JSON).
> Token is always auto-mounted at `/var/run/secrets/kubernetes.io/serviceaccount`.

---

## Domain 4 — Observability

### All 3 Probe Types

```yaml
livenessProbe:                        # fail → container restarts
  exec:
    command: ["cat", "/tmp/healthy"]
  initialDelaySeconds: 5
  periodSeconds: 5

readinessProbe:                       # fail → removed from Service endpoints
  httpGet: {path: /, port: 80}
  initialDelaySeconds: 5

readinessProbe:                       # tcpSocket — third type
  tcpSocket: {port: 80}
  initialDelaySeconds: 5

startupProbe:                         # disables liveness/readiness until passes
  exec: {command: ["cat", "/tmp/started"]}
  failureThreshold: 30
  periodSeconds: 1
```

| Probe | On failure | Use for |
|---|---|---|
| **liveness** | Restarts container | Hung / deadlocked process |
| **readiness** | Removes from Service endpoints | Slow-starting or temporarily busy |
| **startup** | Keeps liveness disabled | Slow-booting apps |

> [!WARNING] liveness vs readiness — most common mix-up
> **liveness** fails → kubelet **kills and restarts** the container
> **readiness** fails → pod stays alive, just gets **no traffic**

### Lifecycle Hooks

```yaml
lifecycle:
  postStart:
    exec: {command: ["sh", "-c", "echo started > /tmp/poststart"]}
  preStop:
    exec: {command: ["sh", "-c", "sleep 5"]}
terminationGracePeriodSeconds: 30
```

> [!NOTE]
> `postStart` → async, NOT guaranteed to run before main process starts
> `preStop` → sync, runs before SIGTERM; counts against `terminationGracePeriodSeconds`

### Debug Commands

```bash
kubectl describe pod <pod>                          # Events — first place always
kubectl logs <pod> --previous                       # prior container instance
kubectl logs <pod> -c <container>                   # specific container
kubectl logs <pod> --all-containers=true

kubectl debug <pod> -it --image=busybox \
  --copy-to=<pod>-debug -- sh                       # for crashlooping pods

kubectl top pods --sort-by=cpu                      # needs metrics-server
kubectl top pods --containers
kubectl top nodes

kubectl get events -n default --sort-by=.lastTimestamp
kubectl get events --field-selector reason=BackOff
```

### Diagnosis Flowchart

```
Pod unhealthy?
└── kubectl describe pod → Events
      ├── ErrImagePull / ImagePullBackOff  → wrong image name or tag
      ├── Liveness probe failed            → wrong path/port, kubectl logs --previous
      ├── Pending                          → no node fits (check resources/taints)
      └── CrashLoopBackOff                → kubectl logs --previous for crash output
```

---

## Domain 5 — Services & Networking

### Service Types — Layered

```
External User
     ↓
LoadBalancer   ← EXTERNAL-IP (<pending> on kind — expected, not a bug)
     ↓
NodePort       ← port on EVERY node (range 30000-32767)
     ↓
ClusterIP      ← virtual IP, cluster-internal only
     ↓
Pod IPs        ← actual backends via kube-proxy iptables rules
```

```bash
kubectl expose deployment web --name=web-clusterip --port=80 --type=ClusterIP
kubectl expose deployment web --name=web-nodeport  --port=80 --type=NodePort
kubectl expose deployment web --name=web-lb        --port=80 --type=LoadBalancer
```

### DNS Resolution

```bash
wget -qO- web-clusterip                             # same namespace only
wget -qO- web-clusterip.default.svc.cluster.local  # FQDN — always works
wget -qO- web-clusterip.default                     # short FQDN — also works
```

> [!WARNING] Short name fails cross-namespace
> A pod in `ns-b` has `ns-b` in its search path, not `default`.
> Always use FQDN (`svc.namespace`) for cross-namespace traffic.

### Port-Forward — Fastest Service Test

```bash
kubectl port-forward svc/web-clusterip 8080:80
curl localhost:8080
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx        # required — without this, controller ignores it
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix         # Prefix = /app/foo matches; Exact = /app only
        backend:
          service: {name: web-clusterip, port: {number: 80}}
```

```bash
# Test host-based ingress without real DNS
curl -H "Host: app.example.com" http://localhost:<nodeport>
```

### NetworkPolicy

**Default deny all:**
```yaml
spec:
  podSelector: {}        # empty = ALL pods in namespace
  policyTypes: [Ingress]
  # no ingress rules = deny everything
```

**Allow from pods:**
```yaml
spec:
  podSelector: {matchLabels: {app: web}}
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector: {matchLabels: {role: frontend}}
    ports:
    - {protocol: TCP, port: 80}
```

**Allow from namespace:**
```bash
kubectl label namespace ns-b purpose=trusted
```
```yaml
  ingress:
  - from:
    - namespaceSelector: {matchLabels: {purpose: trusted}}
```

> [!DANGER] AND vs OR — most commonly wrong on exam
> ```yaml
> # AND — same dash (both must match)
> - from:
>   - namespaceSelector:
>       matchLabels: {purpose: trusted}
>     podSelector:           # ← same indent = AND
>       matchLabels: {role: frontend}
>
> # OR — separate dashes (either matches)
> - from:
>   - namespaceSelector:
>       matchLabels: {purpose: trusted}
>   - podSelector:           # ← new dash = OR
>       matchLabels: {role: frontend}
> ```
> Wrong indentation = policy silently allows too much or too little.

**Egress with DNS:**
```yaml
spec:
  podSelector: {matchLabels: {app: web}}
  policyTypes: [Egress]
  egress:
  - ports:                         # omit 'to' = all destinations (DNS anywhere)
    - {protocol: UDP, port: 53}
    - {protocol: TCP, port: 53}
  - to:
    - podSelector: {matchLabels: {app: backend}}
    ports:
    - {protocol: TCP, port: 8080}
```

> [!DANGER] `to: []` vs omitting `to`
> `to: []` (empty array) = **no destinations** = silently blocks everything
> Omit `to` entirely = **all destinations** = what you want for DNS

---

## Quick Reference — Imperative One-liners

```bash
# Pod
kubectl run mypod --image=nginx $do > pod.yaml
kubectl run tmp --image=busybox -it --rm -- sh              # debug shell, auto-deletes
kubectl run tmp --image=busybox --rm --restart=Never \
  -- wget -qO- web-clusterip                                # one-shot command

# Deployment
kubectl create deployment web --image=nginx --replicas=3
kubectl set image deployment/web nginx=nginx:1.26
kubectl rollout undo deployment/web
kubectl rollout undo deployment/web --to-revision=2

# Service
kubectl expose deployment web --port=80 --type=ClusterIP
kubectl port-forward svc/web 8080:80

# ConfigMap / Secret
kubectl create configmap cm --from-literal=k=v
kubectl create secret generic sec --from-literal=k=v

# Namespace
kubectl create namespace myns
kubectl config set-context --current --namespace=myns

# ResourceQuota / LimitRange (no shortcut — write YAML)

# Labels
kubectl label pod mypod key=value
kubectl label pod mypod key-                                # remove label

# Debug
kubectl describe pod <pod>
kubectl logs <pod> --previous
kubectl exec -it <pod> -- sh
kubectl get events --sort-by=.lastTimestamp
kubectl top pods --sort-by=cpu
```

---

## Gotchas — Know These Cold

> [!WARNING] Common exam traps

| Trap | Correct behaviour |
|---|---|
| `to: []` in egress | Empty array = no destinations. Omit `to` for all destinations |
| `--from-file` vs `--from-env-file` | `--from-file` = 1 key (whole file); `--from-env-file` = 1 key per line |
| Short service name cross-namespace | Fails — use `svc.namespace` or FQDN |
| Missing `ingressClassName: nginx` | Ingress controller silently ignores the resource |
| `:set paste` after insert mode | Must be in **normal mode** before pressing `o` or `i` |
| `namespaceSelector` matches Pod labels | No — matches **Namespace object** labels |
| liveness vs readiness | liveness → restarts; readiness → removes from endpoints |
| `postStart` before main process | Not guaranteed — it runs async |
| Container vs Pod securityContext | Container wins; `fsGroup` is Pod-only |
| `rollout undo` without `--to-revision` | Goes back exactly 1 step only |
| Canary `kubectl expose` selector | Must pass `--selector=app=web` explicitly |
| `kubectl logs` on multi-container pod | Fails without `-c <container>` |
| Tabs in YAML | `:set expandtab` + `:%retab!` in vi |
| `kubectl debug` vs `kubectl exec` | `exec` needs running container; `debug` works on crashloop |
