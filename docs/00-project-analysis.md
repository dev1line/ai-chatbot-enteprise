# 00 — Project Analysis

## 1. Context & Problem

Enterprises (especially the **ODC** model) have:
- A large volume of business documentation, runbooks, and security policies that change continuously.
- Engineers spend a lot of time on manual lookups → slow incident response, reduced operational productivity.
- High security requirements: **Zero Data Leak** — no internal data must leak to public services.

## 2. Analysis per STAR

### Situation
Manual lookups are slow; knowledge is fragmented across many systems (wiki, PDF, DB, monitoring).

### Task
An internal AI assistant that:
- Looks up documents (RAG) + **executes actions** (calls APIs, queries the DB).
- Supports both **text** and **voice**.
- Maintains absolute security.

### Action (technical proposal)
- Python + FastAPI backend, with clear layer separation (Repository Pattern).
- Azure OpenAI as the LLM (compliance-friendly, private VNet).
- RAG: ingest documents → Vector DB; LangChain orchestrates the flow.
- Function Calling: gives the LLM controlled access to the reporting DB / internal APIs.
- STT/TTS using open source (Whisper, HuggingFace) to optimize cost.

### Result (target KPIs)
| Metric | Target |
|---|---|
| Lookup time | ~80% reduction |
| Incident time-to-resolution | Markedly reduced |
| API latency (P95) | < 2s (text), streaming for voice |
| RAG faithfulness (Ragas) | > 0.85 |
| Hallucination rate | Measured & minimized |

## 3. The Breakthrough — "Actionable RAG"

Traditional RAG only **reads** documents. This project adds the ability to **act**:
- Generate & execute SQL (Text-to-SQL) within a sandbox and restricted to `SELECT`.
- Call internal APIs (check container/server, KMS, WAF…).
- Hybrid model: Azure OpenAI for reasoning, HuggingFace for TTS to save cost.

## 3b. Primary Purpose (updated) — Multimodal Search of Released Documents

The core focus of the system is **accurate search over the corpus of RELEASED / IMMUTABLE documents** (immutable, versioned):
- Released documents **do not change** → ensures a stable lookup source that is versioned and auditable.
- **Multimodal**: index & search fully across **images** (diagrams, screenshots), **PDFs** (including scans), and **Excel/CSV** (data tables), not just text/markdown.
- Goal: enable "more complete" lookups — answers synthesized from multiple formats + accurate source citations (file, page, sheet/cell, image region).

> This is the foundation for every feature above: the quality of multimodal search determines the quality of answers and their trustworthiness.

## 3c. Long-term Vision — AI Agent for Automating Requirement Analysis & JIRA

Long-term direction: an **AI Agent** system that supports **BAs (Business Analysts)** and **Change Request management**:
- Automatically **analyze customer requirement documents** (SRS, BRD, emails, specs, multi-format attachments).
- Break them down into **user stories / tasks / sub-tasks**, estimate, and attach acceptance criteria.
- **Create & update JIRA tasks** automatically (via the Atlassian/JIRA API) with human-in-the-loop confirmation.
- Detect & manage **Change Requests**: compare new requirements vs. released ones (using the immutable corpus in section 3b), highlight changes, assess impact, and propose backlog updates.

## 4. Detailed Use Cases

1. **Multimodal Document Search (core)**
   - "Where is the architecture diagram of the payment module in release v2.1?" → search in images/PDFs → answer + cite (file, page, image region).
   - "What is the throughput figure in the benchmark file Q2.xlsx?" → read the Excel table → answer + cite (sheet, cell range).
2. **Ops/Security Bot**
   - "What is the current status of the payment-service container?" → call API → answer.
   - "What is the KMS key rotation policy?" → RAG + citation.
3. **Text-to-SQL Report Bot**
   - "This week's revenue by project?" → generate SQL → query PostgreSQL → read the result (voice).
4. **BA / Requirement Automation (vision)**
   - Upload a customer requirement document → the agent analyzes → proposes a task list → BA reviews → create in JIRA.
   - "Compared to the previous release, what changed in this requirement?" → compare against the immutable corpus → list change requests + impact.

## 5. Risks & Solutions

| Risk | Solution |
|---|---|
| Data leak via public LLM | Azure OpenAI private VNet + Private Link, no-train policy |
| SQL injection / destructive commands (DROP/DELETE) | Whitelist `SELECT`, parameterized queries, schema-aware validation, strict unit tests |
| Hallucination | Mandatory citations, Ragas/TruLens evaluation, guardrails |
| Azure timeout / downtime | Circuit Breaker + Retry + standard fallback message |
| Permissions ("permission hallucination") | RBAC at the tool layer; every action checks the user's scope |
| Voice latency | Streaming responses, optimized Vector DB indexing |
| Released documents edited / version drift | Immutable corpus + checksum/hash + versioning; ingest only through the release process |
| Poor-quality OCR/images (blurry scans) | Vision model + OCR fallback, attach a confidence score, flag risky sources |
| Complex Excel tables (merged cells, formulas) | Structured extraction + preserve sheet/cell references, prioritize computed values |
| Agent creates wrong/extra JIRA tasks | Mandatory human-in-the-loop review before writing; dry-run + audit |

## 6. Scope & Expansion Direction

- **Core/MVP**: Phase 0–5 (**multimodal RAG over the released corpus**, Function Calling, Voice, UI).
- **Hardening**: Phase 6–7 (Testing, Security, Deploy).
- **Future**:
  - Phase 8 — Multi-Agent (LangGraph: SQL agent / Doc agent / Log agent), ODC English Trainer.
  - Phase 9 — AI Agent for analyzing customer requirements + JIRA automation + Change Request management (BA support).

## 7. Related Documents

- [`03-document-search-strategy.md`](03-document-search-strategy.md) — Multimodal search strategy over the immutable corpus.
- [`04-jira-automation-vision.md`](04-jira-automation-vision.md) — AI Agent requirement + JIRA vision.
