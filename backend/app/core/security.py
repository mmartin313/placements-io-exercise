from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "super_secret"
RESET_PASSWORD_SECRET_KEY = "reset_password_super_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_jwt(
    data: dict,
    secret: str,
    lifetime_seconds: Optional[int] = None,
    algorithm: str = ALGORITHM,
) -> str:
    payload = data.copy()
    if lifetime_seconds:
        expire = datetime.utcnow() + timedelta(seconds=lifetime_seconds)
        payload["exp"] = expire
    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_jwt(
    encoded_jwt: str,
    secret: str,
    audience: List[str],
    algorithms: List[str] = [ALGORITHM],
) -> Dict[str, Any]:
    return jwt.decode(
        encoded_jwt,
        secret,
        audience=audience,
        algorithms=algorithms,
    )


def forgot_password(user: User) -> str:
    token_data = {
        "user_id": str(user.id),
        "aud": "placements:password-reset",
    }

    reset_password_token_lifetime_seconds = 3600

    token = generate_jwt(
        token_data,
        RESET_PASSWORD_SECRET_KEY,
        reset_password_token_lifetime_seconds,
    )

    return token


def reset_password(db: Session, user: User, token: str, password: str) -> User:
    try:
        data = decode_jwt(
            token,
            RESET_PASSWORD_SECRET_KEY,
            ["placements:password-reset"],
        )
    except jwt.PyJWTError:
        raise Exception("Invalid token")

    try:
        user.id = data["user_id"]
    except KeyError:
        raise Exception("Invalid email for token")

    if not user.is_active:
        raise Exception("User is not active")

    user.hashed_password = get_password_hash(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
