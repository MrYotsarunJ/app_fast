import jwt
from jwt import InvalidTokenError
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import (HTTPBearer,HTTPAuthorizationCredentials)

bearer_scheme = HTTPBearer(auto_error=False)


with open("public_key.pem", "rb") as f:
    PUBLIC_KEY = f.read()


async def get_valid_user(token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]):
    try:
        payload = jwt.decode(token.credentials, PUBLIC_KEY, algorithms=["RS256"])
        return payload 
    except (InvalidTokenError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=[{"msg": "token invalid"}],
            headers={"WWW-Authenticate": "Bearer"},
        )
