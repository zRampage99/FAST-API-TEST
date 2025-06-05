from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth_handler import create_access_token, verify_token
from repository.db import get_session
from service.auth.token_blacklist_service import is_token_blacklisted

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        token = credentials.credentials

        with next(get_session()) as db:
            if is_token_blacklisted(db, token):
                raise HTTPException(status_code=403, detail="Token has been revoked")


            payload = verify_token(token)
            if payload:
                request.state.new_token = create_access_token({"sub": payload["sub"]})
                return payload

        raise HTTPException(status_code=403, detail="Invalid or expired token.")

    



