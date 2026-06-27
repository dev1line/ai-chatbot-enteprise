from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.core.rbac import require_role
from app.rag.ingestion import content_hash, load_document
from app.rag.retriever import index_chunks
from app.repositories.document_repository import DocumentRepository
from app.schemas.auth import CurrentUser

router = APIRouter(prefix="/api/admin", tags=["admin"])

AdminDep = Annotated[CurrentUser, Depends(require_role("ADMIN"))]


@router.post("/ingest")
async def ingest(
    _: AdminDep,
    file: UploadFile = File(...),
    doc_id: str = Form(...),
    version: str = Form("v1"),
    caption: str | None = Form(None),
) -> dict:
    data = await file.read()
    chunks = load_document(file.filename or "unknown", data, doc_id, version, caption=caption)
    indexed = await index_chunks(chunks)

    doc_type = chunks[0].metadata.get("type", "text") if chunks else "text"
    await DocumentRepository().upsert_metadata(
        doc_id=doc_id,
        version=version,
        source=file.filename or "unknown",
        doc_type=doc_type,
        content_hash=content_hash(data),
        metadata={"chunks": indexed},
    )
    return {
        "doc_id": doc_id,
        "version": version,
        "type": doc_type,
        "chunks_indexed": indexed,
        "content_hash": content_hash(data),
    }


@router.get("/documents")
async def list_documents(_: AdminDep) -> list[dict]:
    docs = await DocumentRepository().list_all()
    return [
        {
            "doc_id": d.docId,
            "version": d.version,
            "source": d.source,
            "type": d.type,
            "content_hash": d.contentHash,
        }
        for d in docs
    ]
