from fastapi import Request, HTTPException


def get_current_user(request: Request):
    user_data = request.state.user
    if not user_data:
        raise HTTPException(401, "No autenticado")
    return user_data 