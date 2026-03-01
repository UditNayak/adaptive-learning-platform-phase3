from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository
from app.utils.security import hash_password, verify_password


class AuthService:

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def signup(self, name: str, email: str, password: str) -> User:
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")

        hashed = hash_password(password)

        user = User(
            name=name,
            email=email,
            password_hash=hashed,
            role=UserRole.USER
        )

        return self.user_repo.create(user)

    def login(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        return user