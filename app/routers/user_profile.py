from fastapi import APIRouter, Depends, HTTPException, status

from app import schemas
from app.dependencies import get_user_profile_dal
from app.storage.user_profile import UserProfileDAL, DuplicateEmail, UserProfileNotFound

router = APIRouter(prefix="/api/profile")


@router.post(
    "/",
    response_model=schemas.UserProfileCreateOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_profile(
    user_profile: schemas.UserProfileCreate,
    user_profile_dal: UserProfileDAL = Depends(get_user_profile_dal),
):
    try:
        user_id = await user_profile_dal.create_user_profile(user_profile)
    except DuplicateEmail as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        ) from exc

    return schemas.UserProfileCreateOut(user_id=user_id)


@router.get(
    "/{user_id}", response_model=schemas.UserProfile, response_model_exclude_none=True
)
async def get_user_profile(
    user_id: int, user_profile_dal: UserProfileDAL = Depends(get_user_profile_dal)
):
    try:
        return await user_profile_dal.get_user_profile(user_id)
    except UserProfileNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found"
        ) from exc


@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_profile(
    user_id: int,
    user_profile_update: schemas.UserProfileUpdate,
    user_profile_dal: UserProfileDAL = Depends(get_user_profile_dal),
):
    try:
        await user_profile_dal.update_user_profile(user_id, user_profile_update)
    except UserProfileNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found"
        ) from exc
    except DuplicateEmail as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        ) from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_profile(
    user_id: int, user_profile_dal: UserProfileDAL = Depends(get_user_profile_dal)
):
    try:
        await user_profile_dal.delete_user_profile(user_id)
    except UserProfileNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found"
        ) from exc
