from fastapi import APIRouter, Request, Depends

from ecommerce_api.schemas import Output, JWTData
from ecommerce_api.errors import NotFound
from ecommerce_api.sql.operations import UserOperations

from ecommerce_api.auth.access import authorize_token, admin_access_only

router = APIRouter(tags=["users"])


@router.get("/users/all", response_model=Output)
@admin_access_only
async def all_users(
    request: Request,
    data: JWTData = Depends(authorize_token)
):
    """
    Returns a list of all signed-up users
    """
    users = UserOperations.get_all()
    return Output(success=True, results=users)


@router.get("/users/{email}", response_model=Output)
@admin_access_only
async def get_user(
    request: Request,
    email: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Returns user info from database
    """
    user = UserOperations.get_by_email(email=email)
    if not user:
        raise NotFound(details="User not found")
    return Output(success=True, results=user)


@router.delete("/users/{email}", response_model=Output)
@admin_access_only
async def delete_user(
    request: Request,
    email: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Returns user info from database
    """
    user = UserOperations.get_by_email(email=email)
    if not user:
        raise NotFound(details="User not found")
    UserOperations.delete(email=email)
    return Output(success=True, message="User deleted")