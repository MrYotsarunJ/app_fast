import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_valid_user(token: Annotated[str, Depends(oauth2_scheme)]):
    with open("public_key.pem", "rb") as f:
        public_key = f.read()

    try:
        payload = jwt.decode(token, public_key, algorithms="RS256")
        return payload
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail=[{"msg": "token invalid"}])
