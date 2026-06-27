# Phase 5 — Frontend / UI Quality

## Context
Backend đã đủ: RAG, Actionable RAG, Voice (text + audio streaming). Giờ xây UI chuyên nghiệp: **Chat Console**, **Hold-to-Talk**, và hiển thị **Citations** bắt buộc.

## Objective
SPA React/Vue + TypeScript: trải nghiệm chat hiện đại, voice hands-free, và minh bạch nguồn (citations) để tăng độ tin cậy.

## Scope
**In:** Chat Console UI, Hold-to-Talk (Web Audio API), citations panel, streaming render, auth UI.
**Out:** thay đổi backend logic.

## Tasks
1. **Chat Console** (`src/components/ChatConsole.tsx`): danh sách message, input, trạng thái loading/streaming, render markdown.
2. **Streaming render** (`src/hooks/useStream.ts`): nhận SSE/WebSocket, render answer dần dần.
3. **Hold-to-Talk** (`src/components/HoldToTalk.tsx` + `src/hooks/useAudio.ts`): nhấn-giữ để ghi (MediaRecorder/Web Audio API), thả ra gửi `POST /api/voice/chat`, phát audio trả lời.
4. **Citations panel** (`src/components/Citations.tsx`): mỗi câu trả lời RAG hiển thị **trích dẫn** (tài liệu, trang, snippet) — bắt buộc, click mở nguồn.
5. **Auth** (`src/components/Login.tsx` + lưu JWT an toàn): gọi API với token, xử lý 401/403.
6. **API client** (`src/api/`): typed client cho chat/voice/auth, xử lý lỗi & fallback message.
7. **UX**: responsive, accessible, trạng thái lỗi rõ ràng, indicator khi đang ghi âm/đang xử lý.

## Deliverables
- ChatConsole, HoldToTalk, Citations, Login, hooks, api client.
- UI kết nối đầy đủ backend (text + voice).

## Acceptance Criteria
- [ ] Gửi câu hỏi text → answer stream dần + citations hiển thị.
- [ ] Nhấn-giữ nói → nhận câu trả lời bằng audio.
- [ ] Câu trả lời RAG **luôn** kèm citations; click xem được nguồn.
- [ ] Xử lý 401/403 và lỗi mạng gracefully.
- [ ] UI responsive & accessible cơ bản (keyboard, aria).

## Guardrails
- Citations là thành phần bắt buộc, không ẩn.
- JWT lưu an toàn (tránh XSS leak); không log token.
- Tôn trọng API contract Phase 4 (content-type, streaming).
