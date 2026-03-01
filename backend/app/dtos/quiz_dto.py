from pydantic import BaseModel
from uuid import UUID
from typing import Dict


class QuizGenerateDTO(BaseModel):
    chat_session_id: UUID


class QuizSubmitDTO(BaseModel):
    quiz_id: UUID
    user_id: UUID
    selected_option: str


class QuizResponseDTO(BaseModel):
    id: UUID
    question_text: str
    options_json: Dict[str, str]
    difficulty: str
    points: int
    hint: str | None
    explanation: str | None

    class Config:
        from_attributes = True