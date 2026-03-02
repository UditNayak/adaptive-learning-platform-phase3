from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.dependencies import get_db
from app.dtos.analytics_dto import UserAnalyticsResponseDTO
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/user/{user_id}", response_model=UserAnalyticsResponseDTO)
def get_user_analytics(user_id: UUID, db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_user_analytics(user_id)