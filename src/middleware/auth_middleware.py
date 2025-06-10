from fastapi import FastAPI, Request, HTTPException, Depends
from jwt import decode, exceptions
from src.security.security import decode_jwt_token, get_current_user

OPEN_URLS = ["/signin", "/login", "/docs", "/openapi.json"]

async def auth_middleware(request: Request, call_next):
    # Excluimos sign-in
    if request.url.path in OPEN_URLS:
        return await call_next(request)

    user = get_current_user(request)
    response = await call_next(request)
    return response
    
def admin_required(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user