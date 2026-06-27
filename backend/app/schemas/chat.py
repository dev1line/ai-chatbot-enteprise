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
    version: str | None = None  # lọc theo version tài liệu (immutable corpus)


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    citations: list[Citation] = []


class SessionResponse(BaseModel):
    id: str
    title: str | None = None
    created_at: str


class SessionListResponse(BaseModel):
    items: list[SessionResponse]


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: str


class MessageListResponse(BaseModel):
    items: list[MessageResponse]
    page: int
    page_size: int


class CompletionUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class CompletionRequest(BaseModel):
    session_id: str
    content: str = Field(min_length=1)


class CompletionResponse(BaseModel):
    session_id: str
    assistant_message: str
    usage: CompletionUsage


class ChatTurn(BaseModel):
    role: str = Field(pattern="^(system|user|assistant)$")
    content: str = ""


class PublicCompletionRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[ChatTurn] = []


class PublicCompletionResponse(BaseModel):
    answer: str
    usage: CompletionUsage
