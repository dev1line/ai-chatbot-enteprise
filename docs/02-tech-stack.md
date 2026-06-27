# 02 — Tech Stack & Rationale

| Layer | Technology | Rationale |
|---|---|---|
| Language | Python 3.11+ | The strongest AI/ML ecosystem |
| Web framework | FastAPI | Async, type-safe (Pydantic), streaming, automatic docs |
| ORM | Prisma (prisma-client-py) | Type-safe, good migrations, separates session logic |
| Database | PostgreSQL | Solid relational model, JSONB, sufficient for Text-to-SQL reporting |
| Orchestration | LangChain | Orchestrates RAG + tool calling, many integrations |
| Embeddings | Azure OpenAI text-embedding-ada-002 | High quality, same Azure ecosystem (compliance) |
| Doc parsing (multimodal) | unstructured, PyMuPDF/pdfplumber, openpyxl/pandas | Structured, layout-aware extraction of PDF/Excel/Word |
| OCR | Tesseract / Azure AI Document Intelligence | Read scanned PDFs & text in images (compliant when using Azure) |
| Vision | Azure OpenAI vision / CLIP-class embeddings | Describe & search across images and diagrams |
| Hybrid search | BM25 (Postgres/Elastic) + dense embeddings + cross-encoder rerank | Captures both exact keywords and semantics, improves precision |
| Vector DB | Pinecone (managed) / Milvus (self-host) | Metadata filtering + namespace by version (immutable corpus) |
| LLM | Azure OpenAI (GPT-4 class) | Private VNet, enterprise compliance, no-train |
| STT | Whisper | Open source, multilingual, accurate |
| TTS | Hugging Face TTS | Open source, cost-optimized, self-hosted |
| Frontend | React (or Vue) + TypeScript | Large ecosystem, easy to hire for |
| Audio | Web Audio API / MediaRecorder | Hold-to-Talk recording in the browser |
| Testing | PyTest | The de-facto standard for Python |
| LLM Eval | Ragas / TruLens | Measure faithfulness, answer relevancy, hallucination |
| Resilience | Circuit Breaker (pybreaker), Retry (tenacity) | Fault tolerance when Azure times out |
| Security | Azure Private Link, VNet, Key Vault | Zero Data Leak, secret management |
| Future | LangGraph / AutoGen | Multi-agent orchestration |
| Issue tracking | JIRA REST API v3 (Atlassian) | Automate creating/updating tasks for BAs, manage change requests |

## Environment Conventions

- Secrets via **Azure Key Vault** / environment variables, NEVER hardcoded.
- `.env.example` describes every required variable.
- Separate config by environment: `dev`, `staging`, `prod`.

## Implementation Principle: LOCAL-FIRST / DOCKER-FIRST

> Important: **It must run locally (via Docker) first.** All development & functional testing (Phase 0–6) runs on **Docker Compose** on the developer's machine. **Azure infrastructure (Phase 7) is only deployed AFTER functionality development is complete.**

- There must be an **environment flag** in ENV to distinguish the run mode:
  - `APP_ENV=local | docker | staging | prod`
  - Providers **swappable via ENV** so local does not strictly depend on Azure.
- Local mode uses **alternatives that run offline/in Docker** (Postgres container, Milvus/Qdrant container, Tesseract OCR, Whisper local, HF TTS local). Azure is only enabled when `APP_ENV` is `staging/prod` or explicitly configured.
- Every script/Makefile target is separated: `make dev-up` (local docker) vs `make infra-*` (Azure — run later).

### Provider abstraction (selected via ENV)

| Variable | Local/Docker | Azure (later) |
|---|---|---|
| `LLM_PROVIDER` | `azure_openai` (can point to a dev key) or mock | `azure_openai` (private VNet) |
| `EMBEDDING_PROVIDER` | `azure_openai` / local | `azure_openai` |
| `VECTOR_DB_PROVIDER` | `milvus` / `qdrant` (container) | `pinecone` / `milvus` |
| `OCR_PROVIDER` | `tesseract` (local) | `azure_doc_intelligence` |
| `STT_PROVIDER` | `whisper_local` | `whisper_local` / azure |
| `TTS_PROVIDER` | `hf_local` | `hf_local` |
| `SECRETS_PROVIDER` | `env` (.env) | `azure_key_vault` |

## Main Environment Variables (example)

```
# --- Run mode / flags ---
APP_ENV=local                 # local | docker | staging | prod
SECRETS_PROVIDER=env          # env | azure_key_vault
LLM_PROVIDER=azure_openai     # azure_openai | mock
EMBEDDING_PROVIDER=azure_openai
VECTOR_DB_PROVIDER=milvus     # milvus | qdrant | pinecone
OCR_PROVIDER=tesseract        # tesseract | azure_doc_intelligence
STT_PROVIDER=whisper_local
TTS_PROVIDER=hf_local

# --- Azure (only enabled in staging/prod or when configured) ---
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT_CHAT=
AZURE_OPENAI_DEPLOYMENT_EMBED=

# --- Vector DB ---
PINECONE_API_KEY=
MILVUS_URI=http://milvus:19530

# --- Core ---
DATABASE_URL=postgresql://app:app@postgres:5432/app
WHISPER_MODEL=base
TTS_MODEL=...
JWT_SECRET=
JIRA_BASE_URL=
JIRA_API_TOKEN=
```
