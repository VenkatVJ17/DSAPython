# CKAD 10-Day Intensive Refresh Plan

Exam date: 2026-06-29 (10 days from today, 2026-06-19)
Daily budget: 3-4 hrs/day
Status: cluster + killer.sh not yet set up — Day 1 covers both

Exam domain weights (current CKAD curriculum):
- Application Environment, Configuration & Security — 25%
- Application Design and Build — 20%
- Application Deployment — 20%
- Services and Networking — 20%
- Application Observability and Maintenance — 15%

Strategy: you've already covered the material once, so each day is ~30% concept refresh + 70% timed hands-on drills. No new theory after Day 7.

---

## Day 1 (Thu 06-19) — Environment + Application Design & Build
- Set up local cluster: `kind create cluster` (or minikube), confirm `kubectl` context, install `vim`/aliases (`alias k=kubectl`, set `KUBE_EDITOR`)
- Register/start killer.sh session access from your exam confirmation email (sessions expire ~36hrs after activation — do NOT activate yet, just confirm you have access)
- Bookmark allowed docs: kubernetes.io/docs, helm.sh/docs, kubernetes.io/docs/reference/kubectl/cheatsheet
- Refresh: Docker image basics, multi-container Pods, Jobs & CronJobs, `kubectl run`/`create` imperative commands
- Drill: write 10 Pod/Job/CronJob manifests from memory, no copy-paste, time yourself (<3 min each)

## Day 2 — Pod Design Patterns
- Refresh: init containers, sidecar, ambassador, adapter patterns; labels/selectors/annotations; resource requests vs limits
- Drill: killercoda.com CKAD scenarios on multi-container pods (free, untimed)
- Practice: convert a single-container Pod spec into init+sidecar pattern in under 5 minutes

## Day 3 — Application Deployment
- Refresh: Deployments, ReplicaSets, rolling updates, rollback (`kubectl rollout undo`), deployment strategies (blue-green, canary via labels), Helm install/upgrade/rollback, Kustomize overlays
- Drill: do a rolling update, force a bad rollout, roll it back — all imperatively, no manifests where possible
- Practice: build one Helm chart from `helm create`, modify values, upgrade, rollback

## Day 4 — Configuration, Security & Environment (heaviest domain — 25%)
- Refresh: ConfigMaps/Secrets (as env vars, volumes, individual keys), SecurityContext (runAsUser, capabilities, fsGroup), ServiceAccounts, ResourceQuotas/LimitRanges
- Drill: 15 fast scenarios mixing ConfigMap-as-volume + Secret-as-env + SecurityContext in one Pod spec
- Practice: `kubectl create configmap`/`create secret` imperative one-liners until automatic

## Day 5 — Observability
- Refresh: liveness/readiness/startup probes (exec, http, tcp), `kubectl debug`, `kubectl logs -f`, `kubectl exec`, container lifecycle hooks (postStart/preStop)
- Drill: take a broken Pod (crashlooping, failing probe) and debug to root cause in <10 min
- Practice: add all 3 probe types to one Deployment without docs

## Day 6 — Services & Networking
- Refresh: ClusterIP/NodePort/LoadBalancer, Ingress + Ingress rules/paths, NetworkPolicies (default-deny, allow-from-namespace), DNS resolution between services
- Drill: NetworkPolicy scenarios — these are the most commonly missed exam questions, do extra reps
- Practice: expose a Deployment 3 ways, write 2 NetworkPolicies (deny-all + allow-specific)

## Day 7 — Integration Review + Killer.sh Session 1
- Morning: rapid-fire review across all 5 domains (flashcard-style, your weakest recall items first)
- Afternoon/evening: **activate killer.sh session 1**, do it as a real timed exam (2 hrs), no docs lookups beyond what's allowed
- After: do NOT review yet — sleep on it

## Day 8 — Killer.sh Session 1 Review + Targeted Repair
- Go through every missed/slow question, identify the *category* of mistake (syntax fumble vs concept gap vs time management)
- Re-drill only the failure categories, 3x repetitions each
- Speed work: practice `kubectl explain`, `--dry-run=client -o yaml`, and editing generated YAML fast in vim

## Day 9 — Killer.sh Session 2 (Full Simulation)
- Activate killer.sh session 2 under strict exam conditions — same time of day as your actual exam slot if possible
- Full review immediately after, since this is your last full practice rep
- Build a one-page personal cheat sheet of commands/aliases you'll mentally rehearse (not for use in exam — for memorization)

## Day 10 (Sat 06-28) — Light Review + Rest
- 1-2 hrs max: skim cheat sheet, re-run 5-10 quick imperative commands to keep muscle memory warm
- Confirm exam logistics: ID, room setup if remote-proctored, browser/lockdown check, exam start buffer time
- No new content. Rest.

---

## Daily habits throughout
- Always solve under time pressure — set a timer per question (~7-10 min) even when "just reviewing"
- Default to imperative `kubectl` commands + `--dry-run=client -o yaml > file.yaml` then edit, rather than writing YAML from scratch
- Use `kubectl config set-context --current --namespace=<ns>` immediately in any practice scenario with a given namespace, to avoid losing points on wrong-namespace mistakes
- Practice navigating kubernetes.io docs search by domain (you're allowed one browser tab to docs only)
