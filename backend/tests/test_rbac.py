from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.core.deps import get_current_user
from app.core.rbac import require_role
from app.schemas.auth import CurrentUser


def _build_app(user_role: str) -> FastAPI:
    app = FastAPI()

    async def fake_user() -> CurrentUser:
        return CurrentUser(id="u1", role=user_role)

    app.dependency_overrides[get_current_user] = fake_user

    @app.get("/admin")
    async def admin_only(_: CurrentUser = Depends(require_role("ADMIN"))):
        return {"ok": True}

    return app


def test_admin_allowed():
    client = TestClient(_build_app("ADMIN"))
    assert client.get("/admin").status_code == 200


def test_viewer_forbidden():
    client = TestClient(_build_app("VIEWER"))
    assert client.get("/admin").status_code == 403
