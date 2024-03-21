import jwt
import time
from jwt.exceptions import InvalidTokenError
from fastapi import FastAPI,Depends,HTTPException,status,Request
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from models import Token


JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_REFRESH_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

def decodeJWT(jwtoken: str):
    try:
        payload = jwt.decode(jwtoken, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload if payload["expires"] >= time.time() else None
    except InvalidTokenError:
        return None
    
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authentication credentials.")
        
    def verify_jwt(self, jwtoken: str)->bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
            
        if payload:
            isTokenValid = True
        return isTokenValid
    
jwt_bearer = JWTBearer()