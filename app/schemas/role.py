# schemas/role.py

from pydantic import BaseModel
from uuid import UUID
from typing import List

class CapabilityRead(BaseModel):
    id: UUID
    name: str
    description: str

    class Config:
        orm_mode = True

class RoleCapabilitiesRead(BaseModel):
    id: UUID
    name: str
    description: str
    capabilities: List[CapabilityRead]

    class Config:
        orm_mode = True