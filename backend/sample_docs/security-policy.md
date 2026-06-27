# Security Policy (Release v2.1)

## KMS Key Rotation
All encryption keys managed by KMS must be rotated periodically, once every 90 days.
The rotation process is automated via a pipeline and must be logged to the audit system.
Old keys are kept in a disabled state for 30 days before being destroyed.

## WAF Rules
The Web Application Firewall blocks common attack patterns: SQL injection, XSS, path traversal.
Any change to WAF rules must go through a change request and be reviewed by the Security team.

## Access Control (RBAC)
Role-based authorization: ADMIN, ENGINEER, VIEWER. Principle of least-privilege.
Production access requires two-level approval.
