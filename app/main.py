from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.exceptions.app_exception import AppError
from app.db import engine
from contextlib import asynccontextmanager
from .api.router import api_router
from .core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: Verifying database connectivity...")
    try:
        with engine.connect() as connection:
            print("Successfully connected to the Supabase PostgreSQL instance!")
    except Exception as e:
        print(f"Database connection failed during startup: {e}")
        raise e
        
    yield
    
    print("Shutting down: Cleaning up database connection pool...")
    engine.dispose()
    print("Shutdown complete.")

app = FastAPI(lifespan=lifespan)

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
