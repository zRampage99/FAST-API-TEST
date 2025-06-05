from fastapi import APIRouter, Depends, Request
from auth.auth_bearer import JWTBearer

health_check_router = APIRouter(
    prefix="/health_check",
    tags=["health_check"],
    dependencies=[Depends(JWTBearer())]
)
@health_check_router.get("")
def jwt_protect():
    return {"message": "Items protected by JWT"}