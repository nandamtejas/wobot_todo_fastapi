from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request=request)

        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(403, "Invalid Authentication Scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(403, "Invalid Token or expired Token")
            return credentials.credentials
        else:
            raise HTTPException(403, "Invalid Authorization code")
    
    def verify_jwt(self, jwttoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwttoken)
        except:
            payload = None 
        if payload:
            isTokenValid = True
        return isTokenValid

