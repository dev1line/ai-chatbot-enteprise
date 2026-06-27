from pydantic import BaseModel, Field


class Citation(BaseModel):
    type: str = "text"  # text | pdf | image | excel
    doc_id: str
    version: str | None = None
    source: str | None = None
    page: int | None = None
    sheet: str | None = None
    cell_range: str | None = None
    bbox: list[float] | None = None
    snippet: str | None = None


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: str | None = None
    version: str | None = None  # filter by document version (immutable corpus)


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    citations: list[Citation] = []
