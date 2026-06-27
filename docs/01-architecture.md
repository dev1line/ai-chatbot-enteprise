# 01 — System Architecture

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

## 2. Main Processing Flows

### A. Text query (RAG)
1. UI sends the question → FastAPI (auth + RBAC).
2. Orchestrator embeds the query (ada-002) → retrieves top-k from the Vector DB.
3. Prompt = context + question → Azure OpenAI.
4. Returns the answer + **citations** (doc id, page).

### B. Actionable query (Function Calling)
1. The LLM receives the tool schema (text_to_sql, internal_api_call).
2. The LLM decides to call a tool → parameters are validated (RBAC + sandbox).
3. The tool executes (only allowed SELECT / API) → result is returned to the LLM → summarized.

### C. Voice
1. UI records audio (Hold-to-Talk) → sends the blob.
2. Whisper STT → text → flow A/B.
3. Answer → HuggingFace TTS → audio stream back to the client.

## 3. Project Directory Structure (proposed implementation)

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
├── docker-compose.yml          # LOCAL-FIRST: full stack runs locally (postgres + vector db + backend + frontend)
├── Makefile                    # dev-up / dev-down / test (local) · infra-* (Azure, Phase 7)
├── .env.example                # APP_ENV flag + swappable providers
├── infra/                      # Azure IaC (terraform, private link) — DEPLOYED LATER (Phase 7)
└── docs/
```

> Note: `docker-compose.yml` at the root serves local development (Phase 0–6, no Azure needed). The `infra/` directory is only used in Phase 7, after functionality development is complete.

## 4. Design Principles

- **Separation of concerns**: API ↔ Orchestration ↔ Repository are cleanly separated.
- **Repository Pattern**: isolates DB access, easy to test/mock.
- **Tool guardrails**: every tool has a schema + validator + RBAC check.
- **Observability-first**: log a trace for every request (query, retrieved docs, tool calls, latency).
- **Resilience**: Circuit Breaker around Azure OpenAI; graceful fallback.
