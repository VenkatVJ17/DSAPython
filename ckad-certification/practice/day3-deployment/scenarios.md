# Day 3 — Application Deployment

## 1. Create + scale (3 min)
Create a Deployment `web` with image `nginx:1.25`, 3 replicas, imperatively. Scale it to 5, then back to 3.

## 2. Rolling update + watch (5 min)
Update `web` to image `nginx:1.26` using `kubectl set image`. Watch the rollout status live. Confirm with `kubectl rollout history`.

## 3. Force a bad rollout and recover (7 min)
Update `web` to a bad image tag (e.g. `nginx:does-not-exist`). Observe `ImagePullBackOff`/stuck rollout. Undo the rollout back to the last working revision. Confirm Pods are healthy again.

## 4. Rollout to a specific revision (5 min)
After at least 3 revisions exist (tag changes count as revisions), use `kubectl rollout undo --to-revision=<n>` to go back to a specific one, not just the previous one. Verify with `kubectl rollout history deployment/web`.

## 5. maxSurge / maxUnavailable (5 min)
Edit `web`'s rollout strategy so `maxSurge=1` and `maxUnavailable=0` (zero downtime rolling update). Trigger another image update and confirm replica count never drops below 3 during the rollout (`kubectl get pods -w` in a second terminal).

## 6. Canary via labels (10 min)
Deploy `web-stable` (3 replicas, label `track=stable`, image `nginx:1.25`) and `web-canary` (1 replica, label `track=canary`, image `nginx:1.26`), both also labeled `app=web`. Create a single Service `web-svc` selecting only `app=web` so traffic splits ~3:1 across both. Confirm via `kubectl get endpoints web-svc`.

## 7. Helm basics (8 min)
`helm create mychart`. Change the replica count and image tag in `values.yaml`. `helm install demo ./mychart`. Confirm Pods. `helm upgrade demo ./mychart --set replicaCount=5`. `helm rollback demo 1`. Confirm replica count reverted.

## 8. Kustomize overlay (5 min)
Create a `base/` with a Deployment + Service, and an `overlay/dev/` that patches the replica count and adds a `env=dev` label via `kustomize`. Apply with `kubectl apply -k overlay/dev`.
