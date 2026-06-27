# 01 — Kiến trúc hệ thống (Architecture)

## 1. High-level Architecture

```
                          ┌─────────────────────────────┐
                          │        Frontend (SPA)        │
                          │   React/Vue + Web Audio API   │
                          │  Chat Console · Hold-to-Talk  │
                          │       Citations panel         │
                          └───────────────┬───────────────┘
                                          │ HTTPS / WebSocket (stream)
                          ┌───────────────▼───────────────┐
                          │      FastAPI API Gateway       │
                          │  Auth (JWT) · RBAC · Rate-limit │
                          │  Circuit Breaker · Retry        │
                          └───────────────┬───────────────┘
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  │                       │                       │
        ┌─────────▼────────┐   ┌──────────▼──────────┐   ┌────────▼────────┐
        │  Voice Service    │   │  Orchestrator        │   │ Repositories     │
        │  Whisper (STT)    │   │  (LangChain)         │   │ (Prisma ORM)     │
        │  HF TTS           │   │  RAG + Tool routing  │   │ PostgreSQL       │
        └───────────────────┘   └──────────┬──────────┘   └─────────────────┘
                                          │
              ┌───────────────────────────┼───────────────────────────┐
              │                           │                           │
   ┌──────────▼─────────┐    ┌────────────▼───────────┐   ┌───────────▼──────────┐
   │  RAG Retriever      │    │  Function Calling Tools │   │   Azure OpenAI        │
   │  Vector DB          │    │  - text_to_sql (SELECT) │   │   (private VNet)      │
   │  (Pinecone/Milvus)  │    │  - internal_api_call    │   │   LLM + ada-002 embed │
   └─────────────────────┘    └─────────────────────────┘   └───────────────────────┘
```

## 2. Luồng xử lý chính

### A. Text query (RAG)
1. UI gửi câu hỏi → FastAPI (auth + RBAC).
2. Orchestrator embed query (ada-002) → retrieve top-k từ Vector DB.
3. Prompt = context + câu hỏi → Azure OpenAI.
4. Trả về answer + **citations** (doc id, page).

### B. Actionable query (Function Calling)
1. LLM nhận tool schema (text_to_sql, internal_api_call).
2. LLM quyết định gọi tool → tham số được validate (RBAC + sandbox).
3. Tool thực thi (chỉ SELECT / API cho phép) → kết quả trả lại LLM → tóm tắt.

### C. Voice
1. UI ghi audio (Hold-to-Talk) → gửi blob.
2. Whisper STT → text → luồng A/B.
3. Answer → HuggingFace TTS → audio stream về client.

## 3. Cấu trúc thư mục dự án (đề xuất triển khai)

```
ai-chatbot-enterprise/
├── backend/
│   ├── app/
│   │   ├── api/                # routers (chat, voice, admin)
│   │   ├── core/               # config, security, RBAC, circuit breaker
│   │   ├── orchestration/      # LangChain/LangGraph chains, prompt templates
│   │   ├── rag/                # ingestion (text/pdf/ocr/image/excel), embeddings, retriever (hybrid+rerank)
│   │   ├── tools/              # function-calling tools (sql, api)
│   │   ├── agents/             # requirement_analyzer, work_breakdown, change_request (Phase 9)
│   │   ├── integrations/       # jira/ (REST API), external systems (Phase 9)
│   │   ├── voice/              # whisper stt, hf tts
│   │   ├── repositories/       # Repository Pattern (Prisma client)
│   │   └── schemas/            # Pydantic models
│   ├── prisma/                 # schema.prisma, migrations
│   ├── tests/                  # pytest, ragas/trulens evals
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/         # ChatConsole, HoldToTalk, Citations
│   │   ├── hooks/              # useAudio, useStream
│   │   └── api/
│   └── package.json
├── docker-compose.yml          # LOCAL-FIRST: full stack chạy local (postgres + vector db + backend + frontend)
├── Makefile                    # dev-up / dev-down / test (local) · infra-* (Azure, Phase 7)
├── .env.example                # flag APP_ENV + provider swappable
├── infra/                      # IaC Azure (terraform, private link) — TRIỂN KHAI SAU (Phase 7)
└── docs/
```

> Lưu ý: `docker-compose.yml` ở root phục vụ dev local (Phase 0–6, không cần Azure). Thư mục `infra/` chỉ dùng ở Phase 7 sau khi dev xong chức năng.

## 4. Nguyên tắc thiết kế

- **Separation of concerns**: API ↔ Orchestration ↔ Repository tách bạch.
- **Repository Pattern**: cô lập truy xuất DB, dễ test/mock.
- **Tool guardrails**: mọi tool có schema + validator + RBAC check.
- **Observability-first**: log trace mỗi request (query, retrieved docs, tool calls, latency).
- **Resilience**: Circuit Breaker quanh Azure OpenAI; fallback graceful.
