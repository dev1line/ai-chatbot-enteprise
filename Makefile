.PHONY: help dev-up dev-down dev-build logs test backend-test fmt lint infra-plan infra-apply

help:
	@echo "LOCAL-FIRST targets:"
	@echo "  make dev-up       - khởi động full stack local (docker compose)"
	@echo "  make dev-down     - dừng & xoá container"
	@echo "  make dev-build    - build lại images"
	@echo "  make logs         - xem logs"
	@echo "  make test         - chạy backend tests trong container"
	@echo "  make fmt          - format (black + ruff --fix)"
	@echo "  make lint         - lint (ruff)"
	@echo ""
	@echo "INFRA targets (Phase 7 - triển khai SAU khi dev xong):"
	@echo "  make infra-plan   - (placeholder) terraform plan"
	@echo "  make infra-apply  - (placeholder) terraform apply"

dev-up:
	@test -f .env || cp .env.example .env
	docker compose up -d --build

dev-down:
	docker compose down

dev-build:
	docker compose build

logs:
	docker compose logs -f --tail=100

test:
	docker compose run --rm backend pytest -q

backend-test:
	cd backend && pytest -q

fmt:
	cd backend && black . && ruff check --fix .

lint:
	cd backend && ruff check .

# --- Phase 7: Azure infra (chưa triển khai ở giai đoạn dev) ---
infra-plan:
	@echo "[infra] Phase 7 — sẽ triển khai sau khi dev xong chức năng."

infra-apply:
	@echo "[infra] Phase 7 — sẽ triển khai sau khi dev xong chức năng."
