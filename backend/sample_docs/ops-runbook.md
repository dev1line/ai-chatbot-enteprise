# Ops Runbook (Release v2.1)

## Check container status
Use the command `kubectl get pods -n payment` to view the status of the payment-service pods.
If a pod is in the CrashLoopBackOff state, check the logs with `kubectl logs`.

## Incident Response process
1. Confirm the impact level (severity).
2. Notify the #incident channel.
3. Isolate the root cause (logs, metrics, traces).
4. Remediate and record a post-mortem within 48 hours.

## Restart the service
Restart safely with a rolling update, no downtime: `kubectl rollout restart deploy/payment-service`.
