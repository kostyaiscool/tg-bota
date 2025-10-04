from typing import TYPE_CHECKING

from pydantic import BaseModel
if TYPE_CHECKING:
    from schemas.permissions import PermissionRead

class RoleRead(BaseModel):
    id: int
    name: str
    desc: str
    permission: list[PermissionRead]

class PermissionCreate(BaseModel):
    name: str
    desc: str

