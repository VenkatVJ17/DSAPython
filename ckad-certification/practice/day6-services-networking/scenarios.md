# Day 6 — Services & Networking (NetworkPolicy is the most commonly missed area — extra reps)

## 1. Expose a Deployment 3 ways (8 min)
Create a Deployment `web` (image `nginx`, 2 replicas). Expose it as:
- ClusterIP service `web-clusterip`
- NodePort service `web-nodeport` (let k8s pick the port, then note it)
- (conceptual only, no real LB available) LoadBalancer service `web-lb`, inspect its `EXTERNAL-IP` staying `<pending>` in kind

## 2. Service DNS resolution (5 min)
From a temporary debug Pod in the same namespace, `curl` or `wget` the ClusterIP service by name (`web-clusterip`) and by FQDN (`web-clusterip.default.svc.cluster.local`). Confirm both resolve.

## 3. Service across namespaces (5 min)
Create namespace `ns-b`. From a Pod in `ns-b`, reach the `web-clusterip` Service living in `default` using its FQDN. Confirm short name alone fails cross-namespace but FQDN works.

## 4. Basic Ingress (7 min)
(If using kind, install an ingress controller first — note as setup step, not part of the timed drill.) Create an Ingress routing path `/app` to `web-clusterip` on port 80. Confirm via the ingress controller's NodePort.

## 5. Default-deny NetworkPolicy (5 min)
Create a NetworkPolicy in `default` namespace that denies all ingress traffic to all Pods (`podSelector: {}`, `policyTypes: [Ingress]`, no `ingress` rules). Confirm a previously-reachable Pod is now unreachable.

## 6. Allow-from-specific-label NetworkPolicy (8 min)
On top of #5, add a second NetworkPolicy allowing ingress to Pods labeled `app=web` only from Pods labeled `role=frontend`, on port 80. Test: a Pod with `role=frontend` can reach it; a Pod without that label cannot.

## 7. Allow-from-namespace NetworkPolicy (7 min)
Create a NetworkPolicy allowing ingress to Pods labeled `app=web` only from any Pod in a namespace labeled `purpose=trusted`. Label `ns-b` with `purpose=trusted`, confirm Pods there can now reach `web`, while Pods in unlabeled namespaces cannot.

## 8. Egress restriction (5 min)
Create a NetworkPolicy restricting egress from a Pod so it can only reach DNS (port 53 UDP/TCP) and one specific Pod/port — confirm all other outbound traffic is blocked.
