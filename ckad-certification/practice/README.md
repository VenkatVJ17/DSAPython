# CKAD Practice Scenarios

Companion to `../CKAD_LEARNING_PLAN.md`. One scenario file per day's domain, solutions kept separate so you can attempt before checking.

## Setup
```
docker info >/dev/null 2>&1 || open -a Docker   # start Docker Desktop first
kind create cluster --config ../kind-config.yaml
kubectl cluster-info --context kind-ckad-practice
kubectl config set-context --current --namespace=default
```

Teardown when done for the day (optional, recreate fresh anytime):
```
kind delete cluster --name ckad-practice
```

## How to use each scenario file
1. Set a timer per task (target time is noted).
2. Solve using imperative `kubectl` commands + `--dry-run=client -o yaml` first; only hand-write YAML when the task requires fields imperative commands can't set.
3. Check your work against `solutions/<day>.md` only after attempting — or after the timer runs out.
4. Run `kubectl delete all --all` between scenarios in a file to reset state, or delete/recreate the namespace.

## Index
- `day2-pod-design/scenarios.md` — init containers, sidecar/ambassador/adapter, labels/selectors
- `day3-deployment/scenarios.md` — Deployments, rollouts/rollbacks, Helm
- `day4-config-security/scenarios.md` — ConfigMaps, Secrets, SecurityContext, quotas
- `day5-observability/scenarios.md` — probes, debugging, lifecycle hooks
- `day6-services-networking/scenarios.md` — Services, Ingress, NetworkPolicies
