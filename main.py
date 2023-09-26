from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from fastapi_jwt_auth import AuthJWT
import inspect, re
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from schemas import Settings
from resources.role import role_router
from resources.role_user import role_user_router
from resources.user_property import property_user_router
from resources.property import property_router
from fastapi_jwt_auth.exceptions import (
    InvalidHeaderError,
    CSRFError,
    JWTDecodeError,
    RevokedTokenError,
    MissingTokenError,
    AccessTokenRequired,
    RefreshTokenRequired,
    FreshTokenRequired
)
from fastapi.exceptions import RequestValidationError
import jwt
from fastapi.responses import JSONResponse
from pydantic import ValidationError

app=FastAPI()

#this is the router connected Place where we connect every router
app.include_router(role_router)
app.include_router(role_user_router)
app.include_router(property_router)
app.include_router(property_user_router)

#this is for Api documentation
def custom_openapi():
    if app.openapi_schema: 
        return app.openapi_schema 

    openapi_schema = get_openapi(
        title = "Fixxy technical services LLC API",
        version = "1.0",
        description = "An API for a Fixxy technical services llc Service",
        routes = app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
        }
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route,"endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint)) or
                re.search("fresh_jwt_required", inspect.getsource(endpoint)) or
                re.search("jwt_optional", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {
                        "Bearer Auth": []
                    }
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


#auth config please   
@AuthJWT.load_config
def get_config():
    return Settings()

app.openapi = custom_openapi

#Every king of Error Handeler for centerally
class CustomException(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code

@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    status_code = getattr(exc, "status_code", 500)  # Get status_code if available, otherwise default to 500
    return JSONResponse(status_code=status_code, content={"message": exc.message})

@app.exception_handler(InvalidHeaderError)
async def invalid_header_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

@app.exception_handler(jwt.InvalidTokenError)
async def invalid_header_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

@app.exception_handler(MissingTokenError)
async def missing_token_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

@app.exception_handler(JWTDecodeError)
async def jwt_decode_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

@app.exception_handler(RefreshTokenRequired)
async def jwt_decode_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

@app.exception_handler(CSRFError)
async def jwt_decode_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

@app.exception_handler(RevokedTokenError)
async def jwt_decode_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

@app.exception_handler(AccessTokenRequired)
async def jwt_decode_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

@app.exception_handler(FreshTokenRequired)
async def jwt_decode_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

@app.exception_handler(jwt.ExpiredSignatureError)
async def jwt_expired_signature_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

# @app.exception_handler(RequestValidationError)
# async def jwt_expired_signature_exception_handler(request, exc):
#     return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


#model Engine
models.Base.metadata.create_all(engine)

#origin set for which port or ip
origins=[
    "*"
]

#this is the middleware place
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)