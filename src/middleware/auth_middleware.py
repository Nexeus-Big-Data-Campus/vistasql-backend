from fastapi import FastAPI, Request, HTTPException
from jwt.exceptions import ExpiredSignatureError, DecodeError
from src.security.security import JWT_SECRET_KEY, decode_jwt_token
from starlette.responses import JSONResponse

OPEN_URLS = ["/sign-in", "/login", "/docs", "/openapi.json","/token"]

async def auth_middleware(request: Request, call_next):
    # Excluimos sign-in y rutas abiertas
    if request.url.path in OPEN_URLS:
        return await call_next(request)

    # Obtener el token del encabezado Authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        print("HEADERS:", request.headers, auth_header)
        return JSONResponse(status_code=401, content={"detail": "Token no proporcionado"})
    
    elif not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Token inválido"})
        
    token = auth_header.split(" ")[1]  # Extraer el token después de "Bearer"
    try:
        # Decodificar el token JWT
        payload = decode_jwt_token(token)
        request.state.user = payload  # Guarda los datos del usuario en el estado de la solicitud
    except ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"detail": "El token ha expirado"})
    except DecodeError:
        return JSONResponse(status_code=401, content={"detail": "Token inválido"})

    # Continuar con la solicitud
    response = await call_next(request)
    return response
