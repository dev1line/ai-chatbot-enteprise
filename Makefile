.PHONY: help dev-up dev-down dev-build logs test backend-test fmt lint infra-plan infra-apply

help:
	@echo "LOCAL-FIRST targets:"
	@echo "  make dev-up       - start the full local stack (docker compose)"
	@echo "  make dev-down     - stop & remove containers"
	@echo "  make dev-build    - rebuild images"
	@echo "  make logs         - view logs"
	@echo "  make test         - run backend tests in the container"
	@echo "  make fmt          - format (black + ruff --fix)"
	@echo "  make lint         - lint (ruff)"
	@echo ""
	@echo "INFRA targets (Phase 7 - deployed AFTER development is complete):"
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

# --- Phase 7: Azure infra (not deployed during the development stage) ---
infra-plan:
	@echo "[infra] Phase 7 — will be deployed after feature development is complete."

infra-apply:
	@echo "[infra] Phase 7 — will be deployed after feature development is complete."
