from typing import TYPE_CHECKING

from pydantic import BaseModel
if TYPE_CHECKING:
    from schemas.roles import RoleRead

class PermissionRead(BaseModel):
    id: int
    name: str
    role: list[RoleRead]
class PermissionCreate(BaseModel):
    name: str
    # role: list[]