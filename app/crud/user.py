import uuid
import requests
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserRead

def create_user(
    session: Session,
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    phone_number: str,
    keycloak_id: str,
) -> UserRead:
    
    # Store user in PostgreSQL
    user = User(
        id=uuid.uuid4(),
        keycloak_id=keycloak_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return UserRead.model_validate(user)

if __name__ == "__main__":

    from app.database import SessionLocal
    session = SessionLocal()

    i = 3
    user_data = {
        "keycloak_id": "94265738-2789-40ae-91bf-915f44325abb",
        "username": f"username-{i}",
        "first_name": f"firstname-{i}",
        "last_name": f"lastname-{i}",
        "email": f"email-{i}@gmail.com",
        "phone_number": "09001234569"
    }

    create_user(
        session, 
        **user_data
    )