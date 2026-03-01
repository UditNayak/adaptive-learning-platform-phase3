from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dtos.user_dto import UserCreateDTO, UserLoginDTO, UserResponseDTO
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserResponseDTO)
def signup(user_data: UserCreateDTO, db: Session = Depends(get_db)):
    try:
        service = AuthService(db)
        user = service.signup(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=UserResponseDTO)
def login(user_data: UserLoginDTO, db: Session = Depends(get_db)):
    try:
        service = AuthService(db)
        user = service.login(
            email=user_data.email,
            password=user_data.password
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))