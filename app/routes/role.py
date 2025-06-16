from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import Role
from app.schemas.role import RoleCapabilitiesRead

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=List[RoleCapabilitiesRead])
def get_roles_with_capabilities(session: Session = Depends(get_db)):
    roles = session.query(Role).all()
    return roles
