---
phase: "04"
slug: voice-pipeline
spec: ".agent/specs/phase-04-voice-pipeline.spec.md"
---

# Phase 04 — Voice Pipeline (TASKS)

> Rules: `.agent/rules/03-task-management.md` + `.agent/rules/00-global.md`.

## Overview table
| Task | Description | Assignee | Status | PR |
|------|-------|----------|--------|----|
| T1 | STT (Whisper) | - | todo | - |
| T2 | TTS (HuggingFace) | - | todo | - |
| T3 | Voice endpoint | - | todo | - |
| T4 | Streaming | - | todo | - |
| T5 | Robustness (timeout/fallback) | - | todo | - |
| T6 | API contract for the frontend | - | todo | - |

---

### T1 — STT (Whisper)
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH04-T1-stt`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/voice/stt.py`: audio blob → Whisper transcribe → text
- [ ] Language detection
- [ ] Select the model via env (`WHISPER_MODEL`)
- [ ] Commit with the `Task: PH04-T1` trailer

**Notes:**

### T2 — TTS (HuggingFace)
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH04-T2-tts`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/voice/tts.py`: text → audio (HuggingFace TTS)
- [ ] Return stream/bytes
- [ ] Select the model/voice via env
- [ ] Commit with the `Task: PH04-T2` trailer

**Notes:**

### T3 — Voice endpoint
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH04-T3-voice-endpoint`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `POST /api/voice/transcribe`: audio → text
- [ ] `POST /api/voice/chat`: audio → STT → orchestrator → answer → TTS → audio stream
- [ ] Commit with the `Task: PH04-T3` trailer

**Notes:**

### T4 — Streaming
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH04-T4-streaming`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Return text chunk by chunk (SSE/WebSocket)
- [ ] Synthesize audio once the LLM finishes processing
- [ ] Commit with the `Task: PH04-T4` trailer

**Notes:**

### T5 — Robustness (timeout/fallback)
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH04-T5-robustness`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Timeout for STT/TTS
- [ ] Fallback to text if TTS fails (no crash)
- [ ] Commit with the `Task: PH04-T5` trailer

**Notes:**

### T6 — API contract for the frontend
- **Assignee:** -
- **Status:** todo
- **Branch:** `docs/PH04-T6-api-contract`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Define request/response, audio content-type
- [ ] Document it for Phase 5 to use
- [ ] Test with a sample audio file
- [ ] Commit with the `Task: PH04-T6` trailer

**Notes:**
