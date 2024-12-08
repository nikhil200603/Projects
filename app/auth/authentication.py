from typing import List

from fastapi import HTTPException, Depends

from app.auth.auth_bearer import JWTBearer

def require_roles(allowed_roles: List[str]):
    def dependency(user: dict = Depends(JWTBearer())):
        if user.get('role') not in allowed_roles:
            raise HTTPException(status_code=403, detail="You do not have permission to perform this action.")
        return user
    return dependency
