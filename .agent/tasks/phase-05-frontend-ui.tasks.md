---
phase: "05"
slug: frontend-ui
spec: ".agent/specs/phase-05-frontend-ui.spec.md"
---

# Phase 05 — Frontend / UI Quality (TASKS)

> Rules: `.agent/rules/02-coding-standards.md` (frontend) + `.agent/rules/00-global.md`.

## Overview table
| Task | Description | Assignee | Status | PR |
|------|-------|----------|--------|----|
| T1 | Chat Console | - | todo | - |
| T2 | Streaming render hook | - | todo | - |
| T3 | Hold-to-Talk | - | todo | - |
| T4 | Citations panel | - | todo | - |
| T5 | Auth UI | - | todo | - |
| T6 | Typed API client | - | todo | - |
| T7 | UX polish | - | todo | - |

---

### T1 — Chat Console
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH05-T1-chat-console`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `src/components/ChatConsole.tsx`: message list + input
- [ ] Loading/streaming state
- [ ] Render markdown
- [ ] Commit with the `Task: PH05-T1` trailer

**Notes:**

### T2 — Streaming render hook
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH05-T2-use-stream`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `src/hooks/useStream.ts`: receive SSE/WebSocket
- [ ] Render the answer gradually
- [ ] Commit with the `Task: PH05-T2` trailer

**Notes:**

### T3 — Hold-to-Talk
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH05-T3-hold-to-talk`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `src/components/HoldToTalk.tsx` + `src/hooks/useAudio.ts`
- [ ] Press-and-hold to record (MediaRecorder/Web Audio API)
- [ ] Release to send `POST /api/voice/chat`
- [ ] Play the answer audio
- [ ] Commit with the `Task: PH05-T3` trailer

**Notes:**

### T4 — Citations panel
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH05-T4-citations`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `src/components/Citations.tsx`: display citations (document, page, snippet)
- [ ] Mandatory for every RAG answer
- [ ] Click to open the source
- [ ] Commit with the `Task: PH05-T4` trailer

**Notes:**

### T5 — Auth UI
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH05-T5-auth-ui`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `src/components/Login.tsx` + store the JWT securely
- [ ] Call the API with the token
- [ ] Handle 401/403
- [ ] Commit with the `Task: PH05-T5` trailer

**Notes:**

### T6 — Typed API client
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH05-T6-api-client`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `src/api/`: typed client for chat/voice/auth
- [ ] Error handling & fallback message
- [ ] Commit with the `Task: PH05-T6` trailer

**Notes:**

### T7 — UX polish
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH05-T7-ux`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Responsive + accessible
- [ ] Clear error states
- [ ] Indicator while recording/processing
- [ ] Commit with the `Task: PH05-T7` trailer

**Notes:**
