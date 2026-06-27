# Prompts — Hướng dẫn sử dụng

Thư mục này chứa các **prompt có cấu trúc** để đưa cho AI coding agent (Cursor, Claude Code, v.v.) thực thi dự án **theo từng phase**. Mỗi phase là một bước build độc lập, có thể kiểm thử trước khi sang phase kế tiếp.

## Thứ tự thực thi

```
phase-00-foundation          → Setup repo, env, Docker
phase-01-backend-core        → FastAPI, Prisma, PostgreSQL, RBAC
phase-02-rag-vectordb        → Multimodal RAG (text/PDF/ảnh/Excel) trên kho Released/Immutable + Citations
phase-03-actionable-rag      → Function Calling (Text-to-SQL, internal API)
phase-04-voice-pipeline      → Whisper STT + HuggingFace TTS + streaming
phase-05-frontend-ui         → Chat Console, Hold-to-Talk, Citations UI
phase-06-testing-robustness  → PyTest, Ragas/TruLens, Circuit Breaker
phase-07-security-deployment → Azure Private Link, VNet, observability, deploy
phase-08-multi-agent-future  → LangGraph multi-agent, ODC English Trainer
phase-09-jira-requirement-agent → AI Agent phân tích requirement → JIRA (BA support), Change Request
```

## Cấu trúc mỗi prompt

Mỗi `prompt.md` gồm:
- **Context**: vị trí trong roadmap, phụ thuộc phase trước.
- **Objective**: mục tiêu phase.
- **Scope (In/Out)**: làm gì, không làm gì.
- **Tasks**: checklist từng bước cụ thể.
- **Deliverables**: file/artifact cần tạo.
- **Acceptance Criteria**: điều kiện hoàn thành.
- **Guardrails**: ràng buộc kỹ thuật / bảo mật.

## Cách dùng

1. Mở file `prompt.md` của phase tương ứng.
2. Copy toàn bộ nội dung làm prompt cho agent (kèm context repo).
3. Để agent hoàn thành **Tasks** và đáp ứng **Acceptance Criteria**.
4. Review + test, rồi chuyển phase tiếp theo.

> Lưu ý: Luôn tuân thủ **Guardrails** (đặc biệt Zero Data Leak, chỉ SELECT cho SQL, RBAC ở tầng tool).
