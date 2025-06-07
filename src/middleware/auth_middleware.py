from fastapi import FastAPI, Request, HTTPException, Depends
from jwt import decode, exceptions
from src.security.security import JWT_SECRET_KEY, decode_jwt_token
from starlette.responses import JSONResponse

OPEN_URLS = ["/signin", "/login", "/docs", "/openapi.json"]

async def auth_middleware(request: Request, call_next):
    # Excluimos sign-in
    if request.url.path in OPEN_URLS:
        return await call_next(request)

    user = get_user_from_auth_header(request.headers)
    response = await call_next(request)
    return response
    

def get_user_from_auth_header(headers):
    auth_header = headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail":"Token no proporcionado o inválido"})
        
    token = auth_header.split(" ")[1]  # Extraer el token después de "Bearer"
    try:
        return decode_jwt_token(token)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(status_code=401, detail="El token ha expirado")
    except exceptions.DecodeError:
        return JSONResponse(status_code=401, detail="Token inválido")

def admin_required(user=Depends(get_user_from_auth_header)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user