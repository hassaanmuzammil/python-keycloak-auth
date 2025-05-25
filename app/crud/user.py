import uuid
import requests
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

def create_user(
    session: Session,
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    phone_number: str,
    keycloak_id: str,
) -> UserRead:

    existing_user = session.query(User).filter(
        (User.keycloak_id == keycloak_id)
    ).first()

    if existing_user:
        if existing_user.deleted_at:
            # User is soft deleted - update the record (undelete)
            existing_user.deleted_at = None
            existing_user.first_name = first_name
            existing_user.last_name = last_name
            existing_user.phone_number = phone_number
            existing_user.email_verified = False
            session.commit()
            session.refresh(existing_user)
            return UserRead.model_validate(existing_user)
        else:
            # User exists and is not deleted - raise error or handle as needed
            raise ValueError("User already exists")

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


def get_user(session: Session, user_id: str):
    user = session.query(User).filter(User.id == user_id, User.deleted_at == None).first()
    if not user:
        raise ValueError("User not found")
    
    return user


def update_user(
    session: Session,
    user_id: str,
    first_name: str = None,
    last_name: str = None,
    phone_number: str = None,
    email_verified: bool = None,
) -> UserRead:
    
    user = get_user(session, user_id)
    
    if not user:
        raise ValueError("User not found")

    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if phone_number is not None:
        user.phone_number = phone_number
    
    print(f"Updating user {user_id} with email_verified={email_verified}")
    if email_verified is not None:
        user.email_verified = email_verified

    session.commit()
    session.refresh(user)

    return UserRead.model_validate(user)


def delete_user(session: Session, user_id: str):

    user = get_user(session, user_id)
    if not user:
        raise ValueError("User not found")

    user.deleted_at = datetime.utcnow()
    session.commit()

    return {"msg": "User deleted successfully"}

if __name__ == "__main__":

    from app.database import SessionLocal
    session = SessionLocal()

    i = 10
    user_data = {
        "keycloak_id": "94265738-2719-40ae-91bf-915f44325abb",
        "username": f"username-{i}",
        "first_name": f"firstname-{i}",
        "last_name": f"lastname-{i}",
        "email": f"email-{i}@gmail.com",
        "phone_number": "09001234576",
        "email_verified": True
    }

    create_user(
        session, 
        **user_data
    )

    # user_data = {
    #     "first_name": f"firstname-{i}-updated",
    #     "last_name": f"lastname-{i}-updated",
    #     "phone_number": "09001234569",
    #     "email_verified": False
    # }

    # update_user(
    #     session, 
    #     "6b542c1e-830e-445f-b1ba-c0a963794935", 
    #     **user_data
    # )

    # delete_user(
    #     session, 
    #     "ad757358-f1cc-47d9-b4a2-b6fb7c759659"
    # )