---
phase: "04"
slug: voice-pipeline
title: "Voice Pipeline (STT + TTS)"
status: todo
depends_on: ["03"]
source_prompt: "prompts/phase-04-voice-pipeline/prompt.md"
---

# Phase 04 — Voice Pipeline (SPEC)

## Context
The backend already answers in text (RAG + Actionable). Add voice: speak → Whisper STT → chat → HuggingFace TTS → audio, with streaming support.

## Objective
Implement the voice pipeline: STT (Whisper), TTS (HuggingFace), a voice endpoint, and a streaming response.

## Scope
- **In:** STT service, TTS service, voice endpoint, streaming, audio formats.
- **Out:** Hold-to-Talk UI (Phase 5 — only define the API contract here).

## Deliverables
- `stt.py`, `tts.py`, `voice.py` endpoints.
- Streaming response for text; audio response.
- Tests with a sample audio file.

## Acceptance Criteria
- [ ] Send audio → receive an accurate transcript (appropriate language).
- [ ] `POST /api/voice/chat` returns a valid audio answer.
- [ ] Streaming text chunks work (SSE/WebSocket).
- [ ] STT/TTS error → fallback to text, no crash.
- [ ] Select the STT/TTS model via ENV.

## Guardrails
- Timeouts for STT/TTS; fallback on error.
- Select the model/voice via env (provider swappable).
- Do not log audio/sensitive content at info level.

## Links
- Tasks: `.agent/tasks/phase-04-voice-pipeline.tasks.md`
- Rules: `.agent/rules/00-global.md`, `.agent/rules/04-security-guardrails.md`
