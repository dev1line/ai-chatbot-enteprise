import pytest

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_roundtrip():
    hashed = hash_password("s3cret!")
    assert hashed != "s3cret!"
    assert verify_password("s3cret!", hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_roundtrip():
    token = create_access_token(subject="user-1", role="ENGINEER")
    payload = decode_access_token(token)
    assert payload["sub"] == "user-1"
    assert payload["role"] == "ENGINEER"


def test_jwt_invalid():
    with pytest.raises(ValueError):
        decode_access_token("not-a-valid-token")
