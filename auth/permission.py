from fastapi import Depends, HTTPException
from auth.auth_bearer import JWTBearer

def require_role(*allowed_roles: str):
    def dependency(payload: dict = Depends(JWTBearer())):
        user_roles = payload.get("roles", [])
        if not any(role in user_roles for role in allowed_roles):
            raise HTTPException(status_code=403, detail="Permission denied")
        return payload  # puoi accedere a username e ruoli dall'endpoint
    return dependency