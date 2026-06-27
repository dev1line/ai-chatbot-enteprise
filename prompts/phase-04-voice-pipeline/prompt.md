# Phase 4 — Voice Pipeline (STT + TTS)

## Context
Backend đã trả lời text (RAG + Actionable). Giờ thêm **giọng nói**: người dùng nói → Whisper STT → luồng chat → HuggingFace TTS → audio trả về, hỗ trợ **streaming** để giảm latency.

## Objective
Triển khai voice pipeline: STT (Whisper), TTS (HuggingFace), endpoint voice, và streaming response.

## Scope
**In:** STT service, TTS service, voice endpoint, streaming, định dạng audio.
**Out:** UI Hold-to-Talk (Phase 5 — chỉ định nghĩa contract API ở đây).

## Tasks
1. **STT** (`app/voice/stt.py`): nhận audio blob → Whisper transcribe → text (+ ngôn ngữ phát hiện). Hỗ trợ chọn model qua env (`WHISPER_MODEL`).
2. **TTS** (`app/voice/tts.py`): text → audio (HuggingFace TTS), trả stream/bytes; chọn model/giọng qua env.
3. **Voice endpoint** (`app/api/voice.py`):
   - `POST /api/voice/transcribe`: audio → text.
   - `POST /api/voice/chat`: audio → STT → orchestrator (RAG/tool) → answer → TTS → audio stream.
4. **Streaming**: trả từng chunk text (SSE/WebSocket) cho người đọc trước, đồng thời tổng hợp audio khi LLM xử lý xong (theo ý "Streaming Response").
5. **Robustness**: timeout cho STT/TTS, fallback trả text nếu TTS lỗi.
6. **Định nghĩa API contract** cho frontend (request/response, content-type audio).

## Deliverables
- `stt.py`, `tts.py`, `voice.py` endpoints.
- Streaming response cho text; audio response.
- Test với file audio mẫu.

## Acceptance Criteria
- [ ] Gửi audio → nhận transcript chính xác (ngôn ngữ phù hợp).
- [ ] `POST /api/voice/chat` trả audio trả lời hợp lệ.
- [ ] Text được stream trước khi audio hoàn tất.
- [ ] TTS lỗi → fallback trả text, không crash.

## Guardrails
- STT/TTS dùng mã nguồn mở (tối ưu chi phí), không gửi audio ra dịch vụ public ngoài Azure.
- Có timeout + fallback (chuẩn bị cho Circuit Breaker Phase 6).
- Không lưu audio thô lâu hơn cần thiết (privacy).
