# Day 3 Solutions

## 1. Create + scale
```
kubectl create deployment web --image=nginx:1.25 --replicas=3
kubectl scale deployment web --replicas=5
kubectl scale deployment web --replicas=3
```

## 2. Rolling update + watch
```
kubectl set image deployment/web nginx=nginx:1.26
kubectl rollout status deployment/web
kubectl rollout history deployment/web
```

## 3. Force a bad rollout and recover
```
kubectl set image deployment/web nginx=nginx:does-not-exist
kubectl get pods   # watch ImagePullBackOff
kubectl rollout undo deployment/web
kubectl rollout status deployment/web
```

## 4. Rollout to a specific revision
```
kubectl rollout history deployment/web
kubectl rollout undo deployment/web --to-revision=2
```

## 5. maxSurge / maxUnavailable
```
kubectl patch deployment web -p '{"spec":{"strategy":{"rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'
kubectl set image deployment/web nginx=nginx:1.27
kubectl get pods -w
```

## 6. Canary via labels
```
kubectl create deployment web-stable --image=nginx:1.25 --replicas=3
kubectl label deployment web-stable track=stable app=web
kubectl create deployment web-canary --image=nginx:1.26 --replicas=1
kubectl label deployment web-canary track=canary app=web
kubectl expose deployment web-stable --name=web-svc --port=80 --selector=app=web
kubectl get endpoints web-svc
```
Note: `kubectl expose` copies the source Deployment's pod-template labels as the selector by default — override with `--selector` if needed, or build the Service YAML directly with `selector: {app: web}`.

## 7. Helm basics
```
helm create mychart
# edit mychart/values.yaml: replicaCount, image.tag
helm install demo ./mychart
kubectl get pods
helm upgrade demo ./mychart --set replicaCount=5
helm rollback demo 1
kubectl get pods   # confirm reverted replica count
```

## 8. Kustomize overlay
```
base/kustomization.yaml        # resources: [deployment.yaml, service.yaml]
overlay/dev/kustomization.yaml # resources: [../../base], patches for replicas + label
kubectl apply -k overlay/dev
```
