# Day 2 — Pod Design Patterns

## 1. Init container gate (5 min)
Create a Pod `web-init` with a main container `nginx` (image `nginx`) and an init container `wait-for-file` (image `busybox`) that sleeps 5 seconds then exits 0, simulating a dependency check before the main container starts.

## 2. Sidecar log shipper (7 min)
Create a Pod `app-sidecar` with:
- container `app` (image `busybox`) running `sh -c "while true; do echo $(date) >> /var/log/app.log; sleep 2; done"`
- container `log-agent` (image `busybox`) running `sh -c "tail -f /var/log/app.log"`
- both sharing an `emptyDir` volume mounted at `/var/log`

Verify with `kubectl logs app-sidecar -c log-agent` that it's tailing the same file.

## 3. Ambassador pattern (7 min)
Create a Pod `ambassador-demo` with:
- container `main` (image `busybox`) that does `wget -qO- localhost:8080` in a loop every 5s
- container `ambassador` (image `nginx`) that listens on port 8080 and proxies (simplify: just confirm nginx is up on 8080 — no real proxy config needed for drill purposes)

Goal of this drill is wiring two containers in one Pod with a shared network namespace, not nginx config correctness.

## 4. Labels & selectors speed round (5 min)
Create 3 Pods: `pod-a` (labels `env=prod,tier=web`), `pod-b` (labels `env=prod,tier=db`), `pod-c` (labels `env=dev,tier=web`).
Then in one command each:
- list only pods with `env=prod`
- list only pods with `tier=web`
- list pods with `env=prod` AND `tier=web`
- add a label `checked=true` to `pod-a` without editing YAML
- remove the `tier` label from `pod-c` without editing YAML

## 5. Adapter pattern (5 min)
Create a Pod `adapter-demo` with:
- container `app` (image `busybox`) writing raw logs to a shared `emptyDir` at `/data/raw.log` (e.g. `sh -c "while true; do echo 'ERROR something happened' >> /data/raw.log; sleep 3; done"`)
- container `adapter` (image `busybox`) that reads `/data/raw.log` and reformats it (e.g. `sh -c "tail -f /data/raw.log | sed 's/^/[NORMALIZED] /'"`)

## 6. Resource requests/limits on a multi-container Pod (5 min)
Take your Pod from #2 (`app-sidecar`) and add resource requests/limits: `app` container gets `requests: cpu=50m,memory=64Mi` / `limits: cpu=100m,memory=128Mi`; `log-agent` gets half of that.
