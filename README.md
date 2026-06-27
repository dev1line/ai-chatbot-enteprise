# Enterprise AI Chatbot — "Actionable RAG" Platform

An internal AI assistant for enterprises (especially the **ODC** — Offshore Development Center model) that helps look up business documentation and security policies and **execute actions** (call APIs, run SQL queries) through both **text** and **voice** — with a **Zero Data Leak** commitment.

> The breakthrough: it doesn't just "read documents and answer" (traditional RAG) but delivers **Actionable RAG** — a chatbot that can take action (call functions / query the DB) safely and with permission control (RBAC).

> **Core purpose**: **multimodal** search across a corpus of **released/immutable** documents — including **images, PDF, Excel** — for more complete and accurate lookups.
>
> **Long-term vision**: an AI Agent that automatically **analyzes customer requirement documents** and **creates tasks in JIRA**, supporting **BAs** and managing **Change Requests**.

---

## 1. Objectives (per STAR)

| | Content |
|---|---|
| **Situation** | Enterprises/ODCs face a large volume of business documentation plus complex security policies. Engineers spend a lot of time on manual lookups → slow incident handling and operations. |
| **Task** | Build an internal AI assistant that supports lookups + action execution via text/voice, integrates with internal systems, and ensures absolute security (Zero Data Leak). |
| **Action** | Python backend (FastAPI), Azure OpenAI as the compliance-friendly "brain", a RAG + Vector DB flow, Function Calling for DB/reporting, and open-source STT & TTS. |
| **Result** | ~80% reduction in lookup time. Hands-free support. Real-time queries in natural language, accurate and secure. |

## 2. Core Features

- **Multimodal Search over the Released/Immutable corpus**: full search across text, **PDF, images (diagrams/screenshots), Excel**; the released document corpus is immutable (versioned + hashed), with citations accurate to the page/sheet/cell/image region.
- **Actionable RAG**: answers from documents + calling APIs / generating & running controlled SQL.
- **Voice Pipeline**: Hold-to-Talk → Whisper (STT) → LLM → HuggingFace (TTS), with streaming support.
- **Mandatory Citations**: every RAG answer must display "Citations" (source page/document) to increase trust.
- **RBAC**: user permission control; "permission hallucination" is blocked at the tool layer.
- **Robustness**: Circuit Breaker + Retry + Fallback when Azure times out.
- **Compliance**: Azure OpenAI inside a private VNet (Azure Private Link), with no training on enterprise data.

## 3. Use Cases

1. **Multimodal Document Search (core)**: look up content located inside images/diagrams, PDFs, and Excel tables of released documents; answer + cite the exact source.
2. **Ops/Security Bot**: safely look up policies (WAF/KMS), check container/server status via API.
3. **Intelligent Reporting (Text-to-SQL)**: "What is this week's revenue by project?" → the bot generates SQL, queries the DB, and reads the result aloud.
4. **BA / Requirement Automation (vision)**: analyze customer requirement documents → propose a backlog → BA reviews → create JIRA tasks; manage change requests based on the immutable corpus.

## 4. Architecture & Tech Stack (summary)

```
[ React/Vue UI ] --(text/audio)--> [ FastAPI Gateway ]
        |                                  |
   Web Audio API                     Auth + RBAC
        |                                  |
   Whisper STT  <-----------------> [ Orchestrator (LangChain) ]
                                          /    |    \
                            [ RAG Retriever ] [ Function Calling ] [ Azure OpenAI ]
                                    |               |        \
                            [ Vector DB ]   [ SQL / Internal APIs ]  embeddings(ada-002)
                            (Pinecone/Milvus)        |
                                              [ PostgreSQL via Prisma ]
        |
   HuggingFace TTS  <--- (audio response stream) ---
```

| Layer | Technology |
|---|---|
| Backend | Python, **FastAPI**, Repository Pattern |
| ORM / DB | **Prisma ORM**, **PostgreSQL** |
| AI Orchestration | **LangChain** |
| Embeddings | Azure OpenAI **text-embedding-ada-002** |
| Vector DB | **Pinecone / Milvus** |
| LLM | **Azure OpenAI** (private VNet) |
| STT | **Whisper** (OpenAI SDK / open-source) |
| TTS | **Hugging Face** TTS |
| Frontend | **React / Vue**, Web Audio API |
| Testing | **PyTest**, **Ragas / TruLens** |
| Resilience | **Circuit Breaker**, Retry, Streaming |
| Security | **Azure Private Link**, VNet |
| Future | Multi-Agent (**LangGraph / AutoGen**) |

## 4b. Implementation Principle: LOCAL-FIRST / DOCKER-FIRST

- Develop & test all functionality (**Phase 0–6**) running **locally via Docker Compose**, with NO dependency on Azure.
- **Azure infrastructure (Phase 7) is deployed LATER**, after the functionality is developed.
- Distinguish environments via the **ENV flag** `APP_ENV` (`local|docker|staging|prod`) + swappable providers (`LLM_PROVIDER`, `VECTOR_DB_PROVIDER`, `OCR_PROVIDER`, `SECRETS_PROVIDER`...). Changing environments = changing flags, not editing logic.
- Commands: `make dev-up` (run locally), `make infra-*` (Azure — done later). Details: `docs/02-tech-stack.md`, section "LOCAL-FIRST".

## 5. Roadmap by Phase

| Phase | Name | Main Goal | Prompt |
|---|---|---|---|
| **0** | Foundation & Setup | Repo, env, Docker, basic CI | [`prompts/phase-00-foundation`](prompts/phase-00-foundation/prompt.md) |
| **1** | Backend Core & Architecture | FastAPI, Prisma, PostgreSQL, RBAC, Repository Pattern | [`prompts/phase-01-backend-core`](prompts/phase-01-backend-core/prompt.md) |
| **2** | Multimodal RAG (Released/Immutable) | Ingest text/PDF/images/Excel → embeddings → Vector DB (versioned) → hybrid search + rerank + multimodal citations | [`prompts/phase-02-rag-vectordb`](prompts/phase-02-rag-vectordb/prompt.md) |
| **3** | Actionable RAG (Function Calling) | Safe Text-to-SQL + calling internal APIs via tools | [`prompts/phase-03-actionable-rag`](prompts/phase-03-actionable-rag/prompt.md) |
| **4** | Voice Pipeline | Whisper STT + HuggingFace TTS + streaming | [`prompts/phase-04-voice-pipeline`](prompts/phase-04-voice-pipeline/prompt.md) |
| **5** | Frontend / UI | Chat Console, Hold-to-Talk, Citations | [`prompts/phase-05-frontend-ui`](prompts/phase-05-frontend-ui/prompt.md) |
| **6** | Testing & Robustness | PyTest, Ragas/TruLens, Circuit Breaker, Fallback | [`prompts/phase-06-testing-robustness`](prompts/phase-06-testing-robustness/prompt.md) |
| **7** | Security & Deployment | Azure Private Link, VNet, observability, deploy | [`prompts/phase-07-security-deployment`](prompts/phase-07-security-deployment/prompt.md) |
| **8** | Multi-Agent & Future | LangGraph orchestrator, ODC English Trainer | [`prompts/phase-08-multi-agent-future`](prompts/phase-08-multi-agent-future/prompt.md) |
| **9** | JIRA & Requirement Automation | AI Agent that analyzes requirements → backlog → JIRA (BA support), Change Request | [`prompts/phase-09-jira-requirement-agent`](prompts/phase-09-jira-requirement-agent/prompt.md) |

## 6. Documentation

- [`docs/00-project-analysis.md`](docs/00-project-analysis.md) — Detailed analysis per STAR + risks.
- [`docs/01-architecture.md`](docs/01-architecture.md) — System architecture & data flow.
- [`docs/02-tech-stack.md`](docs/02-tech-stack.md) — Tech stack & rationale for choices.
- [`docs/03-document-search-strategy.md`](docs/03-document-search-strategy.md) — Multimodal search strategy over the immutable corpus.
- [`docs/04-jira-automation-vision.md`](docs/04-jira-automation-vision.md) — AI Agent requirement + JIRA vision.

## 7. How to Use the Prompt Set

See [`prompts/README.md`](prompts/README.md). Each phase has a `prompt.md` file to hand to an AI coding agent for sequential execution (Phase 0 → 8).
