# Day 6 Solutions

## 1. Expose a Deployment 3 ways
```
kubectl create deployment web --image=nginx --replicas=2
kubectl expose deployment web --name=web-clusterip --port=80 --type=ClusterIP
kubectl expose deployment web --name=web-nodeport --port=80 --type=NodePort
kubectl expose deployment web --name=web-lb --port=80 --type=LoadBalancer
kubectl get svc web-nodeport   # note the auto-assigned NodePort
kubectl get svc web-lb         # EXTERNAL-IP stays <pending> on kind (no cloud LB)
```

## 2. Service DNS resolution
```
kubectl run debug --image=busybox -it --rm -- sh
# inside:
wget -qO- web-clusterip
wget -qO- web-clusterip.default.svc.cluster.local
```

## 3. Service across namespaces
```
kubectl create namespace ns-b
kubectl run debug -n ns-b --image=busybox -it --rm -- sh
# inside:
wget -qO- web-clusterip                                       # fails (not in default ns)
wget -qO- web-clusterip.default.svc.cluster.local              # works
```

## 4. Basic Ingress
```
# install ingress-nginx for kind first (one-time setup, not timed)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: {name: web-ingress}
spec:
  rules:
  - http:
      paths:
      - path: /app
        pathType: Prefix
        backend:
          service: {name: web-clusterip, port: {number: 80}}
```

## 5. Default-deny NetworkPolicy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny}
spec:
  podSelector: {}
  policyTypes: [Ingress]
```

## 6. Allow-from-specific-label
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: allow-frontend}
spec:
  podSelector:
    matchLabels: {app: web}
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector:
        matchLabels: {role: frontend}
    ports:
    - {protocol: TCP, port: 80}
```

## 7. Allow-from-namespace
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: allow-trusted-ns}
spec:
  podSelector:
    matchLabels: {app: web}
  policyTypes: [Ingress]
  ingress:
  - from:
    - namespaceSelector:
        matchLabels: {purpose: trusted}
```
```
kubectl label namespace ns-b purpose=trusted
```

## 8. Egress restriction
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: restrict-egress}
spec:
  podSelector: {matchLabels: {app: web}}
  policyTypes: [Egress]
  egress:
  - to: []
    ports:
    - {protocol: UDP, port: 53}
    - {protocol: TCP, port: 53}
  - to:
    - podSelector: {matchLabels: {app: backend}}
    ports:
    - {protocol: TCP, port: 8080}
```
