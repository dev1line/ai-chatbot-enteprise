# Phase 8 — Multi-Agent & Future Enhancements

## Context
MVP đã production-ready (Phase 0–7) với 1 LLM điều phối RAG + tools. Phase này **nâng cấp kiến trúc Multi-Agent** và bổ sung use case mở rộng (ODC English Trainer). Đây là phase định hướng tương lai, làm khi cần scale độ phức tạp.

## Objective
Thay 1 LLM điều phối bằng **Multi-Agent** (LangGraph/AutoGen) để tăng độ chính xác; thêm module phụ "Giao tiếp ODC" (English Trainer).

## Scope
**In:** orchestrator multi-agent, sub-agents chuyên trách, ODC English Trainer.
**Out:** viết lại các tầng đã ổn định (tái sử dụng tools/RAG hiện có).

## Tasks
1. **Multi-Agent orchestration** (`app/orchestration/graph.py` — LangGraph):
   - **Main Agent (Orchestrator)**: phân việc, tổng hợp.
   - **Sub-Agent SQL**: chuyên Text-to-SQL (dùng lại `sql_tool` Phase 3).
   - **Sub-Agent Docs**: chuyên RAG tài liệu (dùng lại retriever Phase 2).
   - **Sub-Agent Logs/Ops**: chuyên check logs/trạng thái hệ thống (dùng `api_tool`).
2. **Định tuyến & hợp nhất**: orchestrator quyết định gọi (các) sub-agent, gộp kết quả, đảm bảo citations vẫn được giữ.
3. **Đánh giá**: so sánh độ chính xác multi-agent vs single-agent qua eval harness Phase 6 (chứng minh cải thiện).
4. **ODC English Trainer** (`app/features/english_trainer.py`):
   - Tận dụng voice pipeline (Phase 4): mô phỏng hội thoại tiếng Anh với khách hàng.
   - Nhận diện & sửa lỗi ngữ pháp/phát âm; gợi ý cách diễn đạt theo ngành.
   - Prompt engineering cho persona "khách hàng/đồng nghiệp nước ngoài".
5. **Feature flag**: bật/tắt multi-agent & english trainer qua config (không phá MVP).

## Deliverables
- LangGraph multi-agent orchestrator + sub-agents.
- Báo cáo so sánh độ chính xác.
- Module ODC English Trainer (voice-based).

## Acceptance Criteria
- [ ] Multi-agent xử lý đúng truy vấn hỗn hợp (vừa doc vừa SQL/logs).
- [ ] Eval cho thấy độ chính xác ≥ single-agent.
- [ ] Citations vẫn được bảo toàn qua orchestrator.
- [ ] English Trainer thực hiện hội thoại voice + phản hồi sửa lỗi.
- [ ] Có feature flag, không ảnh hưởng luồng MVP khi tắt.

## Guardrails
- Tái sử dụng tools/RAG/voice đã kiểm thử, không trùng lặp logic.
- Giữ guardrails bảo mật (RBAC tool-level, chỉ SELECT, Zero Data Leak).
- Multi-agent không làm tăng latency vượt ngưỡng SLA — đo bằng eval/metrics.
