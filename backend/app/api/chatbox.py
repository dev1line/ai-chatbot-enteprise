from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["chatbox"])

_STATIC_DIR = Path(__file__).resolve().parents[1] / "static"


@router.get("/chatbox")
async def chatbox() -> FileResponse:
    return FileResponse(_STATIC_DIR / "chatbox.html")
