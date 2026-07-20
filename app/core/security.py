from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext


SECRET_KEY = "YOUR_SECRET_KEY"

ALGORITHM = "HS256"


ACCESS_TOKEN_EXPIRE_MINUTES = 15

REFRESH_TOKEN_EXPIRE_DAYS = 7


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired"
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )

def hash_password(password:str):

    return pwd_context.hash(password)


def verify_password(
    password,
    hashed_password
):

    return pwd_context.verify(
        password,
        hashed_password
    )


def create_access_token(data:dict):

    payload = data.copy()

    payload.update(
        {
            "exp":
            datetime.utcnow()
            +
            timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            ),

            "type":"access"
        }
    )


    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token(data:dict):

    payload = data.copy()

    payload.update(
        {
            "exp":
            datetime.utcnow()
            +
            timedelta(
                days=REFRESH_TOKEN_EXPIRE_DAYS
            ),

            "type":"refresh"
        }
    )


    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
