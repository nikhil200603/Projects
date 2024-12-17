from typing import List

from fastapi import HTTPException, Depends

from auth.auth_bearer import JWTBearer
from pydantic_models import UserSchema

def require_roles(allowed_roles: List[str]):
    def dependency(user: dict = Depends(JWTBearer())):
        user_data = UserSchema.from_dict(user)
        if user.get('role') not in allowed_roles:
            raise HTTPException(status_code=403, detail="You do not have permission to perform this action.")
        return user_data
    return dependency
