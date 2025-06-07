from fastapi import Request, Depends, HTTPException
from src.middleware.auth_middleware import get_current_user_from_request  

def get_current_user(request: Request = Depends()):
    user_data = request.state.user
    if not user_data:
        raise HTTPException(401, "No autenticado")
    return user_data 