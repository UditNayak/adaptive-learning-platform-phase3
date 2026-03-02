from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dtos.reference_dto import ReferenceRequestDTO, ReferenceResponseDTO
from app.services.reference_service import ReferenceService

router = APIRouter(prefix="/references", tags=["References"])


@router.post("/", response_model=ReferenceResponseDTO)
def get_references(data: ReferenceRequestDTO, db: Session = Depends(get_db)):
    try:
        service = ReferenceService(db)
        return service.get_references(data.chat_session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
