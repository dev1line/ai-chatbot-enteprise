"""RAG Orchestrator: retrieve → build context → LLM generate → answer + citations.

Citations are MANDATORY: return the source (doc_id/version/page/sheet/cell_range/snippet).
If there is no context → respond safely (do not fabricate).
"""
from __future__ import annotations

from app.core.logging import get_logger
from app.orchestration.llm import get_llm_provider
from app.rag.retriever import retrieve
from app.schemas.chat import Citation

logger = get_logger(__name__)

_SYSTEM = (
    "You are an enterprise internal assistant. ONLY answer based on the CONTEXT provided "
    "from the released document repository. If the context does not contain enough information, "
    "clearly state that it cannot be found in the documents instead of fabricating. "
    "Answer concisely and accurately, in English."
)


def _build_context(hits) -> tuple[str, list[Citation]]:
    blocks: list[str] = []
    citations: list[Citation] = []
    for i, h in enumerate(hits, start=1):
        p = h.payload
        text = p.get("text", "")
        blocks.append(f"[{i}] (doc={p.get('doc_id')} v={p.get('version')}) {text}")
        citations.append(
            Citation(
                type=p.get("type", "text"),
                doc_id=p.get("doc_id", "unknown"),
                version=p.get("version"),
                source=p.get("source"),
                page=p.get("page"),
                sheet=p.get("sheet"),
                cell_range=p.get("cell_range"),
                snippet=p.get("snippet"),
            )
        )
    return "\n\n".join(blocks), citations


async def answer_query(query: str, version: str | None = None) -> tuple[str, list[Citation]]:
    hits = await retrieve(query, version=version)
    if not hits:
        return (
            "No relevant information was found in the released document repository.",
            [],
        )
    context, citations = _build_context(hits)
    user_prompt = f"CONTEXT:\n{context}\n\nQUESTION: {query}\n\nAnswer (with references [number]):"
    llm = get_llm_provider()
    answer = await llm.generate(_SYSTEM, user_prompt)
    return answer, citations
