from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dtos.quiz_dto import QuizGenerateDTO, QuizSubmitDTO, QuizResponseDTO
from app.services.quiz_service import QuizService
from app.models.chat_session import ChatSession

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.post("/generate", response_model=QuizResponseDTO)
def generate_quiz(data: QuizGenerateDTO, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(
        ChatSession.id == data.chat_session_id
    ).first()

    service = QuizService(db)
    return service.generate_quiz(session)


@router.post("/submit")
def submit_quiz(data: QuizSubmitDTO, db: Session = Depends(get_db)):
    service = QuizService(db)
    return service.submit_answer(
        quiz_id=data.quiz_id,
        user_id=data.user_id,
        selected_option=data.selected_option
    )