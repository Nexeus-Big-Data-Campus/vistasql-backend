from fastapi import FastAPI, Request, HTTPException
from jwt import decode, exceptions
from src.security.security import JWT_SECRET_KEY, decode_jwt_token



async def auth_middleware(request: Request, call_next):
    # Excluimos sign-in
    if request.url.path in ["/sign-in", "/docs", "/openapi.json"]:
        return await call_next(request)

    # Obtener el token del encabezado Authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado o inválido")

    token = auth_header.split(" ")[1]  # Extraer el token después de "Bearer"

    try:
        # Decodificar el token JWT
        payload = decode_jwt_token(token)
        #payload = decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        request.state.user = payload  # Guarda los datos del usuario en el estado de la solicitud
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Token inválido")

    # Continuar con la solicitud
    response = await call_next(request)
    return response