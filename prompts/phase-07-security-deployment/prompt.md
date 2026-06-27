# Phase 7 — Security & Deployment

## Context
Hệ thống đã chức năng đầy đủ + test (Phase 0–6) và **đã chạy ổn định local qua Docker**. ĐÂY LÀ PHASE TRIỂN KHAI HẠ TẦNG — **chỉ làm SAU khi dev xong chức năng**. Giờ **hardening bảo mật** (Zero Data Leak) và **triển khai** lên Azure với compliance.

> Nguyên tắc: dev/test trước trên Docker local (Phase 0–6); infra Azure ở phase này. Chuyển môi trường chỉ bằng đổi flag `APP_ENV=staging|prod` + `SECRETS_PROVIDER=azure_key_vault` + provider, KHÔNG sửa logic nghiệp vụ.

## Objective
Đảm bảo cam kết Zero Data Leak (Azure Private Link/VNet), quản lý secret, observability, và pipeline triển khai — nâng cấp từ bản local-docker bằng cách đổi flag/provider, không viết lại chức năng.

## Scope
**In:** Azure Private Link/VNet, Key Vault, IaC (Terraform), observability, deployment, hardening.
**Out:** thêm tính năng mới.

## Tasks
0. **Tiền đề**: xác nhận stack đã chạy ổn local qua Docker (Phase 0–6). Phase này chỉ thêm lớp infra + đổi flag/provider để lên Azure; giữ khả năng chạy local nguyên vẹn.
1. **Network (Q&A: Bảo mật dữ liệu)**: Azure OpenAI qua **Private Endpoint/Private Link** trong VNet; backend không gọi public endpoint. Tài liệu hóa cam kết no-train (Enterprise compliance).
2. **Secrets**: chuyển toàn bộ secret sang **Azure Key Vault**; app đọc qua managed identity. Loại bỏ secret khỏi env file prod.
3. **IaC** (`infra/terraform/`): VNet, subnet, private endpoint, Postgres, Key Vault, container apps/AKS.
4. **Vector DB**: nếu yêu cầu on-prem → Milvus self-host trong VNet; nếu Pinecone → đánh giá compliance/region.
5. **Observability**: structured logs tập trung, tracing (request → retrieved docs → tool calls → latency), metrics (Time-to-resolution, API latency P95), dashboard + alert.
6. **Hardening**: HTTPS/TLS, security headers, rate limiting, input validation, dependency scan, least-privilege DB role (read-only cho SQL tool).
7. **Deploy pipeline**: build image, migration Prisma tự động, blue/green hoặc rolling; env `staging` & `prod`.
8. **Runbook**: tài liệu vận hành + rollback.

## Deliverables
- Terraform infra (VNet + Private Link + Key Vault + DB).
- Observability (logs/metrics/traces) + alerts.
- CD pipeline + runbook.

## Acceptance Criteria
- [ ] Azure OpenAI truy cập **chỉ** qua private endpoint (không public).
- [ ] Không secret nào nằm trong code/repo; tất cả ở Key Vault.
- [ ] Metric latency & time-to-resolution hiển thị trên dashboard.
- [ ] SQL tool dùng DB role read-only.
- [ ] Deploy staging/prod chạy migration tự động, có rollback.

## Guardrails
- **Chỉ triển khai sau khi dev xong chức năng** (Phase 0–6 đã chạy ổn local-docker).
- Chuyển môi trường bằng **flag/provider** (`APP_ENV`, `SECRETS_PROVIDER`), KHÔNG viết lại logic.
- **Zero Data Leak**: không endpoint public cho LLM/dữ liệu nội bộ.
- Least privilege ở mọi tầng (DB, network, identity).
- Mọi thay đổi hạ tầng qua IaC (không click tay trên portal).
