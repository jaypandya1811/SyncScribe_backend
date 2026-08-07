from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.exceptions.app_exception import AppError
from app.db import engine
from contextlib import asynccontextmanager
from .api.router import api_router
from .core.logger import logger
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as connection:
            print("Successfully connected to the Supabase PostgreSQL instance!")
    except Exception as e:
        print(f"Database connection failed during startup: {e}")
        raise e
        
    yield
    
    engine.dispose()
    print("Shutdown complete.")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.7:3000",
    "http://192.168.1.10:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.exception_handler(AppError)
def app_error_handler(request: Request, exc: AppError):
    logger.error(f"[{exc.error_code}] {exc.default_message} path={request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error_code, "message": exc.default_message},
    )

@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error at {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "message": "An unexpected error occurred."},
    )
