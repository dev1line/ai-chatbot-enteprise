from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, chat, health
from app.core.config import get_settings
from app.core.db import connect_db, disconnect_db
from app.core.logging import configure_logging, get_logger

settings = get_settings()
configure_logging(settings.debug)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Starting %s (APP_ENV=%s)", settings.app_name, settings.app_env)
    try:
        await connect_db()
    except Exception as exc:  # noqa: BLE001
        # Cho phép app khởi động (vd /health) ngay cả khi DB chưa sẵn sàng ở dev.
        logger.warning("DB not connected at startup: %s", exc)
    yield
    await disconnect_db()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(chat.router)
