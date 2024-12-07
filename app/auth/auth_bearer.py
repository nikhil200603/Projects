import time
import traceback

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from config import JwtCred

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return self.verify_jwt(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> dict:
        try:
            decoded_token = jwt.decode(jwtoken, JwtCred.JWT_SECRET, algorithms=[JwtCred.JWT_ALGORITHM])
            return decoded_token if (decoded_token["expires"] > time.time() and decoded_token["token_type"]==JwtCred.ACCESS_TOKEN) else None     # condition to check if it is access token or not
        except Exception as _:
            print(traceback.format_exc())
            raise HTTPException(status_code=404, detail="User info not found")
