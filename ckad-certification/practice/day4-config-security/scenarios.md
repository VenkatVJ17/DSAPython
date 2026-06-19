# Day 4 — Configuration, Security & Environment (25% of exam — drill extra here)

## 1. ConfigMap from literals + file (4 min)
Create a ConfigMap `app-config` with literal keys `LOG_LEVEL=debug` and `MAX_CONNECTIONS=100`. Separately create `app-config-file` from a local file you write containing `key1=value1\nkey2=value2`.

## 2. Consume ConfigMap as env vars (5 min)
Create a Pod `cm-env-pod` (image `busybox`, command `sh -c "env; sleep 3600"`) that injects all keys from `app-config` as environment variables via `envFrom`. Verify with `kubectl exec` + `env`.

## 3. Consume ConfigMap as a volume (5 min)
Create a Pod `cm-vol-pod` mounting `app-config` as a volume at `/etc/config`. Verify each key became a file with `kubectl exec cm-vol-pod -- ls /etc/config` and `cat`.

## 4. Secret from literals + env injection (5 min)
Create a Secret `db-secret` with keys `username=admin` and `password=s3cr3t`. Create a Pod injecting `password` as env var `DB_PASSWORD` (single key, not envFrom) and confirm it's base64-decoded correctly at runtime.

## 5. SecurityContext at Pod and container level (8 min)
Create a Pod `secure-pod` with:
- Pod-level `securityContext`: `runAsUser: 1000`, `runAsGroup: 3000`, `fsGroup: 2000`
- one container overriding with its own `securityContext`: `runAsUser: 2000`, `allowPrivilegeEscalation: false`, `capabilities.drop: ["ALL"]`

Verify `id` inside the container matches the override, not the Pod-level value.

## 6. ResourceQuota + LimitRange (7 min)
Create a Namespace `quota-test`. Add a `ResourceQuota` capping total `pods: 3` and `requests.cpu: 1`. Add a `LimitRange` setting a default `cpu` request/limit for containers that don't specify one. Create Pods without resource specs and confirm the LimitRange default got applied (`kubectl describe pod`), then try to exceed the quota and confirm it's rejected.

## 7. ServiceAccount + mount (5 min)
Create a ServiceAccount `app-sa`. Create a Pod using `serviceAccountName: app-sa`. Confirm the token is auto-mounted at `/var/run/secrets/kubernetes.io/serviceaccount`.

## 8. Speed round — imperative one-liners (5 min)
Without looking anything up, write the one-liner imperative command for each:
- create a Secret from two literal key/value pairs
- create a ConfigMap from an entire directory of files
- create a Secret of type `docker-registry`
- generate a Pod YAML via `--dry-run=client -o yaml` without creating it
