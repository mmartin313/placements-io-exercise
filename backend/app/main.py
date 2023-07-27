import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.api.routers.auth import auth_router
from app.api.routers.invoice_router import invoice_router

from app.core import config
from app.db.session import SessionLocal

app = FastAPI(
    title=config.PROJECT_NAME,
    openapi_url="/api" if config.ENVIRONMENT == "DEVELOPMENT" else None,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

origins = [
    "http://localhost:3001",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


app.include_router(
    auth_router,
    prefix="/api",
    tags=["auth"],
)

app.include_router(
    invoice_router,
    prefix="/api/invoices",
    tags=["Invoice Management"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
