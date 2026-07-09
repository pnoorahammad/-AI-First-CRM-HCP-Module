from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import settings
from app.database.session import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables are created
    create_tables()
    yield
    # Shutdown logic if any


app = FastAPI(
    title="AI-First CRM HCP Module",
    description="CRM backend with LangGraph powered AI capabilities",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import auth, hcp, interactions, chat, tools


@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


@app.get("/")
def root():
    return {"status": "ok", "message": "AI-First CRM HCP Module API is running"}


# Include routers
app.include_router(auth.router)
app.include_router(hcp.router)
app.include_router(interactions.router)
app.include_router(chat.router)
app.include_router(tools.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
